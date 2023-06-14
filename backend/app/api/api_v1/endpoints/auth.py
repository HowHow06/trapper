from app import crud, schemas
from app.api import deps
from app.core import auth as AuthHelper
from app.core.config import settings
from app.models import User as UserModel
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.post("/login", response_model=schemas.Token)
async def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(deps.get_db)):
    # use OAuth2PasswordRequestForm to support authorization in openapi docs
    user = await crud.crud_user.authenticate(
        db, username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password")

    access_token = AuthHelper.create_access_token(user.id)
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        max_age=settings.COOKIE_MAX_AGE_IN_MS,
        httponly=True,
        # samesite="none",
        # secure=settings.ENVIRONMENT != "dev"
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=schemas.UserCreate)
async def register(user_in: schemas.UserCreate, db: AsyncSession = Depends(deps.get_db)):
    user = await crud.crud_user.get_by_email_or_username(db, email=user_in.email, username=user_in.username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this username already exists in the system.",
        )
    return await crud.crud_user.create(db, obj_in=user_in)


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Successfully logged out"}


@router.post("/test-token", response_model=schemas.User)
async def test_token(current_user: UserModel = Depends(deps.get_current_active_user)):
    """
    Test access token
    """
    return current_user
