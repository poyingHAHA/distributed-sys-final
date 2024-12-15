from fastapi import APIRouter, Depends, BackgroundTasks, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func
from datetime import datetime, timedelta
from typing import Optional

from app.database import get_db
from app.models import Checkin, Team, TeamMember, User, TeamCheckinHistory
from app.schemas import CheckinCreate, CheckinResponse
from app.api.dependencies import get_current_user
from app.api.core.exceptions import TeamError, CheckinError, DatabaseError
from app.schemas import DataResponse

router = APIRouter()

async def calculate_team_score_background(team_id: int, completed_round_id: int, db: Session):
    """計算團隊分數的背景任務"""
    team = db.query(Team).filter_by(team_id=team_id).first()
    if not team:
        return

    # 獲取該輪次的所有打卡記錄
    completed_checkins = db.query(Checkin).filter(
        Checkin.team_id == team_id,
        Checkin.round_id == completed_round_id
    ).all()

    if not completed_checkins:
        return

    # 獲取打卡時間範圍
    checkin_times = [checkin.checkin_time for checkin in completed_checkins]
    time_span = (max(checkin_times) - min(checkin_times)).total_seconds() / 60

    # 獲取上一輪打卡記錄
    last_history = db.query(TeamCheckinHistory).filter(
        TeamCheckinHistory.team_id == team_id,
        TeamCheckinHistory.round_id < completed_round_id
    ).order_by(TeamCheckinHistory.round_id.desc()).first()

    # 計算新成員數
    previous_users = set()
    if last_history:
        previous_checkins = db.query(Checkin).filter(
            Checkin.team_id == team_id,
            Checkin.round_id == last_history.round_id
        ).all()
        previous_users = {checkin.user_id for checkin in previous_checkins}

    current_users = {checkin.user_id for checkin in completed_checkins}
    new_members = len(current_users - previous_users)

    # 計算成員權重
    member_weights = {}
    for checkin in completed_checkins:
        total_teams = db.query(TeamMember).filter_by(user_id=checkin.user_id).count()
        member_weights[checkin.user_id] = 1 / total_teams

    total_weights = sum(member_weights.values())

    # 計算分數
    alpha = 1.0  # 時間權重
    beta = 2.0   # 新成員權重
    score = total_weights / (alpha * (time_span + 1)) + beta * new_members

    try:
        # 更新團隊分數
        team.current_score = score

        # 記錄打卡歷史
        history = TeamCheckinHistory(
            team_id=team_id,
            completed_at=datetime.utcnow(),
            member_count=len(completed_checkins),
            round_id=completed_round_id
        )
        db.add(history)
        db.commit()

    except SQLAlchemyError as e:
        db.rollback()
        raise DatabaseError.operation_failed("update_team_score", {"error": str(e)})

@router.post("/checkin", response_model=DataResponse[CheckinResponse])
async def create_checkin(
    checkin: CheckinCreate,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """處理成員打卡"""
    # 檢查團隊和成員資格
    team = db.query(Team).filter_by(team_id=checkin.team_id).first()
    if not team:
        raise TeamError.team_not_found(checkin.team_id)

    team_member = db.query(TeamMember).filter(
        TeamMember.team_id == checkin.team_id,
        TeamMember.user_id == current_user.user_id
    ).first()

    if not team_member:
        raise TeamError.not_team_member(current_user.user_id, checkin.team_id)

    try:
        # 記錄打卡
        db_checkin = Checkin(
            team_id=checkin.team_id,
            user_id=current_user.user_id,
            post_url=checkin.post_url,
            checkin_time=datetime.utcnow(),
            round_id=team.current_round_id
        )
        db.add(db_checkin)
        db.commit()
        db.refresh(db_checkin)

        # 檢查是否所有成員都已打卡
        total_members = db.query(TeamMember).filter_by(team_id=team.team_id).count()
        current_round_checkins = db.query(Checkin).filter(
            Checkin.team_id == team.team_id,
            Checkin.round_id == team.current_round_id
        ).count()

        # 如果所有成員都已打卡
        is_round_complete = current_round_checkins >= total_members
        if is_round_complete:
            # 觸發計分
            background_tasks.add_task(
                calculate_team_score_background,
                team.team_id,
                team.current_round_id,
                db
            )
            # 進入下一輪
            team.current_round_id += 1
            db.commit()

        return DataResponse(
            success=True,
            message="Checkin successful",
            data=CheckinResponse(
                checkin_id=db_checkin.checkin_id,
                team_id=db_checkin.team_id,
                user_id=db_checkin.user_id,
                post_url=db_checkin.post_url,
                checkin_time=db_checkin.checkin_time,
                is_team_complete=is_round_complete
            )
        )

    except SQLAlchemyError as e:
        db.rollback()
        raise DatabaseError.operation_failed("create_checkin", {"error": str(e)})

@router.get(
    "/checkin/status/{team_id}",
    response_model=DataResponse[dict],
    summary="Get team checkin status",
    description="Get the current checkin status for a team"
)
async def get_team_checkin_status(
    team_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    team = db.query(Team).filter_by(team_id=team_id).first()
    if not team:
        raise TeamError.team_not_found(team_id)

    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)

    # Get checkin statistics
    total_members = db.query(TeamMember).filter_by(team_id=team_id).count()
    checked_in_members = db.query(Checkin).filter(
        Checkin.team_id == team_id,
        Checkin.checkin_time >= today_start
    ).distinct(Checkin.user_id).count()

    return DataResponse(
        success=True,
        message="Team checkin status retrieved",
        data={
            "team_id": team_id,
            "total_members": total_members,
            "checked_in_members": checked_in_members,
            "completion_percentage": (checked_in_members / total_members * 100) if total_members > 0 else 0,
            "is_complete": total_members == checked_in_members
        }
    )
