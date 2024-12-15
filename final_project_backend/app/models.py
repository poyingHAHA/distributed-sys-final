# models.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_checkin_time = Column(DateTime)

    teams = relationship("TeamMember", back_populates="user")
    checkins = relationship("Checkin", back_populates="user")

class Team(Base):
    __tablename__ = 'teams'
    team_id = Column(Integer, primary_key=True)
    team_name = Column(String(100), nullable=False)
    creator_id = Column(Integer, ForeignKey('users.user_id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    current_score = Column(Float, default=0.0)
    current_round_id = Column(Integer, default=0)  # 當前輪次
    members = relationship("TeamMember", back_populates="team")
    checkins = relationship("Checkin", back_populates="team")
    checkin_histories = relationship("TeamCheckinHistory", back_populates="team")
    # 默认排序规则
    # __mapper_args__ = {
    #     "order_by": current_score.desc()  # 按 current_score 倒序排列
    # }


class TeamMember(Base):
    __tablename__ = 'team_members'
    team_id = Column(Integer, ForeignKey('teams.team_id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    joined_at = Column(DateTime, default=datetime.utcnow)
    team = relationship("Team", back_populates="members")
    user = relationship("User", back_populates="teams")

class Checkin(Base):
    __tablename__ = 'checkins'
    checkin_id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey('teams.team_id'))
    user_id = Column(Integer, ForeignKey('users.user_id'))
    post_url = Column(String(255), nullable=False)
    checkin_time = Column(DateTime, default=datetime.utcnow)
    round_id = Column(Integer, nullable=False)
    team = relationship("Team", back_populates="checkins")
    user = relationship("User", back_populates="checkins")

class TeamCheckinHistory(Base):
    __tablename__ = 'team_checkin_history'
    id = Column(Integer, primary_key=True, autoincrement=True)
    team_id = Column(Integer, ForeignKey('teams.team_id'), nullable=False)
    completed_at = Column(DateTime, default=datetime.utcnow)
    member_count = Column(Integer, nullable=False)
    round_id = Column(Integer, nullable=False)
    team = relationship("Team", back_populates="checkin_histories")
