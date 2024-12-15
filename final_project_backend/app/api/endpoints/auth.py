from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from app.database import get_db
from app.api.core.security import create_access_token, verify_password, get_password_hash
from app.api.core.config import settings
from app.models import User
from app.schemas import UserCreate, TokenResponse, UserResponse
from app.api.core.exceptions import AuthError
from app.schemas import DataResponse

router = APIRouter()

@router.post(
    "/register",
    response_model=DataResponse[TokenResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Register new user",
    description="Register a new user and return access token"
)
async def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    # Check if user exists
    if db.query(User).filter(User.username == user.username).first():
        raise AuthError.user_exists()

    # Create new user
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        name=user.name,
        password=hashed_password
    )

    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except Exception as e:
        db.rollback()
        raise AuthError.registration_failed(str(e))

    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )

    return DataResponse(
        success=True,
        message="User registered successfully",
        data=TokenResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user=UserResponse(
                user_id=db_user.user_id,
                username=db_user.username,
                name=db_user.name
            )
        )
    )

@router.post(
    "/token",
    response_model=DataResponse[TokenResponse],
    summary="User login",
    description="Login with username and password to get access token"
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # Verify user credentials
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise AuthError.credentials_exception()

    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )

    return DataResponse(
        success=True,
        message="Login successful",
        data=TokenResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user=UserResponse(
                user_id=user.user_id,
                username=user.username,
                name=user.name
            )
        )
    )