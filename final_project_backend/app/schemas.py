from pydantic import BaseModel, ConfigDict
from typing import Generic, TypeVar, Optional, Any, List
from datetime import datetime

T = TypeVar('T')

# Base Response Models
class ResponseBase(BaseModel):
    success: bool
    message: str

class DataResponse(ResponseBase, Generic[T]):
    data: T

class PaginatedResponse(ResponseBase, Generic[T]):
    data: List[T]
    total: int
    page: int
    size: int

# User Models
class UserBase(BaseModel):
    username: str
    name: str
    model_config = ConfigDict(from_attributes=True)

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    password: Optional[str] = None

class UserResponse(UserBase):
    user_id: int
    last_checkin_time: Optional[datetime] = None

# Authentication Models
class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int

class TokenResponse(Token):
    user: UserResponse

# Team Models
class TeamBase(BaseModel):
    team_name: str
    model_config = ConfigDict(from_attributes=True)

class TeamCreate(TeamBase):
    pass

class TeamUpdate(TeamBase):
    pass

class TeamResponse(TeamBase):
    team_id: int
    creator_id: int
    current_score: float = 0.0
    member_count: int

class TeamDetailResponse(TeamResponse):
    members: List[UserResponse]

class TeamRankingResponse(TeamResponse):
    rank: int

# Checkin Models
class CheckinBase(BaseModel):
    team_id: int
    post_url: str
    model_config = ConfigDict(from_attributes=True)

class CheckinCreate(CheckinBase):
    pass

class CheckinResponse(CheckinBase):
    checkin_id: int
    user_id: int
    checkin_time: datetime
    is_team_complete: bool
    

class MemberResponse(BaseModel):
    user_id: int
    username: str
    name: Optional[str]  # Include this field if required
    last_checkin_time: Optional[str]
