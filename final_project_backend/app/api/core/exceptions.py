from fastapi import HTTPException, status
from typing import Any, Dict, Optional
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


def add_error_handlers(app: FastAPI):
    @app.exception_handler(APIException)
    async def api_exception_handler(request: Request, exc: APIException):
        return JSONResponse(
            status_code=exc.status_code,
            content=exc.detail
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error_code": ErrorCode.UNKNOWN_ERROR,
                "message": "An unexpected error occurred",
                "details": {"error": str(exc)} if app.debug else {}
            }
        )
class ErrorCode:
    """Error code constants"""
    # Auth related errors (1xxx)
    INVALID_CREDENTIALS = "1001"
    USER_EXISTS = "1002"
    INVALID_TOKEN = "1003"
    TOKEN_EXPIRED = "1004"

    # Team related errors (2xxx)
    TEAM_NOT_FOUND = "2001"
    NOT_TEAM_MEMBER = "2002"
    ALREADY_TEAM_MEMBER = "2003"
    TEAM_FULL = "2004"

    # Checkin related errors (3xxx)
    INVALID_CHECKIN = "3001"
    DUPLICATE_CHECKIN = "3002" # Not used in this project
    CHECKIN_NOT_FOUND = "3003"

    # General errors (9xxx)
    VALIDATION_ERROR = "9001"
    DATABASE_ERROR = "9002"
    UNKNOWN_ERROR = "9999"

class APIException(HTTPException):
    """Base API Exception"""
    def __init__(
        self,
        status_code: int,
        error_code: str,
        message: str,
        details: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None
    ):
        self.error_code = error_code
        self.details = details or {}

        super().__init__(
            status_code=status_code,
            detail={
                "error_code": error_code,
                "message": message,
                "details": self.details
            },
            headers=headers
        )

class AuthError:
    """Authentication related errors"""
    @staticmethod
    def credentials_exception(message: str = "Could not validate credentials"):
        return APIException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code=ErrorCode.INVALID_CREDENTIALS,
            message=message,
            headers={"WWW-Authenticate": "Bearer"}
        )

    @staticmethod
    def user_exists():
        return APIException(
            status_code=status.HTTP_409_CONFLICT,
            error_code=ErrorCode.USER_EXISTS,
            message="Username already exists"
        )

class TeamError:
    """Team related errors"""
    @staticmethod
    def team_not_found(team_id: int):
        return APIException(
            status_code=status.HTTP_404_NOT_FOUND,
            error_code=ErrorCode.TEAM_NOT_FOUND,
            message=f"Team with id {team_id} not found",
            details={"team_id": team_id}
        )

    @staticmethod
    def not_team_member(user_id: int, team_id: int):
        return APIException(
            status_code=status.HTTP_403_FORBIDDEN,
            error_code=ErrorCode.NOT_TEAM_MEMBER,
            message="User is not a member of this team",
            details={
                "user_id": user_id,
                "team_id": team_id
            }
        )

    @staticmethod
    def already_team_member(user_id: int, team_id: int):
        return APIException(
            status_code=status.HTTP_409_CONFLICT,
            error_code=ErrorCode.ALREADY_TEAM_MEMBER,
            message="User is already a member of this team",
            details={
                "user_id": user_id,
                "team_id": team_id
            }
        )

class CheckinError:
    """Checkin related errors"""
    @staticmethod
    def duplicate_checkin(user_id: int, team_id: int):
        return APIException(
            status_code=status.HTTP_409_CONFLICT,
            error_code=ErrorCode.DUPLICATE_CHECKIN,
            message="User has already checked in today",
            details={
                "user_id": user_id,
                "team_id": team_id
            }
        )

    @staticmethod
    def invalid_checkin(reason: str):
        return APIException(
            status_code=status.HTTP_400_BAD_REQUEST,
            error_code=ErrorCode.INVALID_CHECKIN,
            message=f"Invalid checkin: {reason}"
        )

class DatabaseError:
    """Database related errors"""
    @staticmethod
    def operation_failed(operation: str, details: Dict[str, Any] = None):
        return APIException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code=ErrorCode.DATABASE_ERROR,
            message=f"Database operation failed: {operation}",
            details=details
        )