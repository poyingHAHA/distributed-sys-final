from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional, List

from app.database import get_db
from app.models import Team, TeamMember, User
from app.schemas import TeamCreate, TeamResponse, TeamDetailResponse, TeamRankingResponse, MemberResponse
from app.api.dependencies import get_current_user
from app.api.core.exceptions import TeamError, DatabaseError
from app.schemas import DataResponse, PaginatedResponse

router = APIRouter()

@router.post(
    "/teams",
    response_model=DataResponse[TeamResponse],
    status_code=201,
    summary="Create new team",
    description="Create a new team and automatically join as creator"
)
async def create_team(
    team: TeamCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        db_team = Team(
            team_name=team.team_name,
            creator_id=current_user.user_id
        )
        db.add(db_team)
        db.flush()

        # Add creator as team member
        team_member = TeamMember(
            team_id=db_team.team_id,
            user_id=current_user.user_id
        )
        db.add(team_member)

        db.commit()
        db.refresh(db_team)

        return DataResponse(
            success=True,
            message="Team created successfully",
            data=TeamResponse(
                team_id=db_team.team_id,
                team_name=db_team.team_name,
                creator_id=db_team.creator_id,
                current_score=0.0,
                member_count=1
            )
        )
    except SQLAlchemyError as e:
        db.rollback()
        raise DatabaseError.operation_failed("create_team", {"error": str(e)})

@router.post(
    "/teams/{team_id}/join",
    response_model=DataResponse[dict],
    summary="Join team",
    description="Join an existing team"
)
async def join_team(
    team_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    team = db.query(Team).filter(Team.team_id == team_id).first()
    if not team:
        raise TeamError.team_not_found(team_id)

    existing_member = db.query(TeamMember).filter(
        TeamMember.team_id == team_id,
        TeamMember.user_id == current_user.user_id
    ).first()

    if existing_member:
        # raise TeamError.already_team_member(current_user.user_id, team_id)
        return DataResponse(
            success=True,
            message="You are already a member of this team",
            data={"team_id": team_id, "user_id": current_user.user_id}
        )

    try:
        team_member = TeamMember(
            team_id=team_id,
            user_id=current_user.user_id
        )
        db.add(team_member)
        db.commit()

        return DataResponse(
            success=True,
            message="Successfully joined team",
            data={"team_id": team_id, "user_id": current_user.user_id}
        )
    except SQLAlchemyError as e:
        db.rollback()
        raise DatabaseError.operation_failed("join_team", {"error": str(e)})

# 獲取所有team_name與team_id
@router.get(
    "/teams/all",
    response_model=DataResponse[List[dict]],
    summary="Get all team names",
    description="Get a list of all team names and IDs"
)
async def get_all_teams(
    db: Session = Depends(get_db)
):
    teams = db.query(Team).all()
    team_list = [{"team_id": team.team_id, "team_name": team.team_name} for team in teams]

    return DataResponse(
        success=True,
        message="All team names retrieved successfully",
        data=team_list
    )

@router.get(
    "/teams/rankings",
    response_model=PaginatedResponse[TeamRankingResponse],
    summary="Get team rankings",
    description="Get paginated team rankings sorted by score"
)
async def get_rankings(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    min_score: Optional[float] = Query(None, ge=0),
    db: Session = Depends(get_db)
):
    query = db.query(Team).options(
        joinedload(Team.members)
    )

    # 如果有最小分數限制
    if min_score is not None:
        query = query.filter(Team.current_score >= min_score)

    # 計算總數
    total_count = query.count()

    teams = (query
        .order_by(Team.current_score.desc())
        .offset((page - 1) * size)
        .limit(size)
        .all()
    )

    rankings = []
    start_rank = (page - 1) * size + 1

    for idx, team in enumerate(teams):
        rankings.append(
            TeamRankingResponse(
                team_id=team.team_id,
                team_name=team.team_name,
                creator_id=team.creator_id,
                current_score=team.current_score,
                member_count=len(team.members),
                rank=start_rank + idx
            )
        )

    return PaginatedResponse(
        success=True,
        message="Team rankings retrieved successfully",
        data=rankings,
        total=total_count,
        page=page,
        size=size
    )

@router.get(
    "/teams/{team_id}",
    response_model=DataResponse[TeamDetailResponse],
    summary="Get team details",
    description="Get detailed information about a specific team"
)
async def get_team(
    team_id: int,
    db: Session = Depends(get_db)
):
    # 獲取團隊詳細資訊，包含成員資訊
    team = db.query(Team).options(
        joinedload(Team.members).joinedload(TeamMember.user)
    ).filter(Team.team_id == team_id).first()

    if not team:
        raise TeamError.team_not_found(team_id)

    # 轉換成員資訊
    members = [
        MemberResponse(
            user_id=member.user.user_id,
            username=member.user.username,
            name=member.user.name,  # Ensure this field is included
            last_checkin_time=member.user.last_checkin_time
        )
        for member in team.members
    ]

    return DataResponse(
        success=True,
        message="Team details retrieved successfully",
        data=TeamDetailResponse(
            team_id=team.team_id,
            team_name=team.team_name,
            creator_id=team.creator_id,
            current_score=team.current_score,
            member_count=len(team.members),
            members=members
        )
    )

@router.get(
    "/teams",
    response_model=PaginatedResponse[TeamResponse],
    summary="Get all teams",
    description="Get a paginated list of all teams with basic information"
)
async def get_teams(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    sort_by: Optional[str] = Query(None, enum=["name", "score", "members"]),
    sort_desc: bool = Query(True, description="Sort in descending order"),
    db: Session = Depends(get_db)
):
    query = db.query(Team).options(
        joinedload(Team.members)
    )

    # 搜尋功能
    if search:
        search_term = f"%{search}%"
        query = query.filter(Team.team_name.ilike(search_term))

    # 排序功能
    if sort_by:
        if sort_by == "name":
            order_by = Team.team_name.desc() if sort_desc else Team.team_name
        elif sort_by == "score":
            order_by = Team.current_score.desc() if sort_desc else Team.current_score
        elif sort_by == "members":
            # 這裡需要子查詢來計算成員數量
            member_count = (
                db.query(TeamMember.team_id, db.func.count(TeamMember.user_id).label('member_count'))
                .group_by(TeamMember.team_id)
                .subquery()
            )
            query = query.outerjoin(member_count, Team.team_id == member_count.c.team_id)
            order_by = member_count.c.member_count.desc() if sort_desc else member_count.c.member_count
        query = query.order_by(order_by)
    else:
        # 默認按創建時間排序
        query = query.order_by(Team.created_at.desc() if sort_desc else Team.created_at)

    # 計算總數
    total_count = query.count()

    # 獲取分頁數據
    teams = query.offset((page - 1) * size).limit(size).all()

    # 轉換為響應格式
    team_responses = [
        TeamResponse(
            team_id=team.team_id,
            team_name=team.team_name,
            creator_id=team.creator_id,
            current_score=team.current_score,
            member_count=len(team.members)
        )
        for team in teams
    ]

    return PaginatedResponse(
        success=True,
        message="Teams retrieved successfully",
        data=team_responses,
        total=total_count,
        page=page,
        size=size
    )
