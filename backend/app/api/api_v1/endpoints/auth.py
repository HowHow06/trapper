from datetime import datetime, timedelta

from app import crud, schemas
from app.api import deps
from app.core import auth as AuthHelper
from app.core.auth import (generate_password, generate_password_reset_token,
                           send_reset_password_email,
                           send_reset_password_success_email, verify_password,
                           verify_password_reset_token)
from app.core.config import settings
from app.models import User as UserModel
from fastapi import APIRouter, Body, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.post("/login", response_model=schemas.Token)
async def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(deps.get_db)):
    user_temp = await crud.crud_user.get_by_username(db, username=form_data.username)

    if user_temp is None or not user_temp:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password")

    # If the user_temp has been blocked within the last 30 minutes
    if user_temp.blocked_at and user_temp.blocked_at > datetime.utcnow() - timedelta(minutes=30):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Too many failed attempts, try again later")

    # If the user_temp has been blocked but not within the last 30 minutes
    if user_temp.blocked_at and not user_temp.blocked_at > datetime.utcnow() - timedelta(minutes=30):
        await crud.crud_user.reset_login_trial(db, db_obj=user_temp)

    # use OAuth2PasswordRequestForm to support authorization in openapi docs
    user = await crud.crud_user.authenticate(
        db, username=form_data.username, password=form_data.password
    )

    if not user:
        if user_temp is not None:
            await crud.crud_user.increment_login_trial(db, db_obj=user_temp)
            user_temp = await crud.crud_user.get_by_username(db, username=form_data.username)
            if user_temp.login_trial >= 3:
                await crud.crud_user.block_user(db, db_obj=user_temp)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password")

    await crud.crud_user.reset_login_trial(db, db_obj=user)
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


@router.post("/register", response_model=schemas.User)
async def register(user_in: schemas.UserRegister, db: AsyncSession = Depends(deps.get_db)):
    user = await crud.crud_user.get_by_email_or_username(db, email=user_in.email, username=user_in.username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this username or email already exists.",
        )
    user_in_data = user_in.dict()
    user_in_data["is_admin"] = False
    user_in_data = schemas.UserCreate(**user_in_data)

    return await crud.crud_user.create(db, obj_in=user_in_data)


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


@router.put("/edit-password", response_model=schemas.User)
async def edit_password(
    password_edit: schemas.UserPasswordEdit,
    current_user: UserModel = Depends(deps.get_current_active_user),
    db: AsyncSession = Depends(deps.get_db),
):
    if not verify_password(
        password_edit.old_password, current_user.hashed_password
    ):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Original password is incorrect")

    user_in_data = current_user.dict()
    user_in_data["password"] = password_edit.new_password
    user_in_data = schemas.UserUpdate(**user_in_data)

    # Update the password
    return await crud.crud_user.update(db, db_obj=current_user, obj_in=user_in_data)


@router.post("/password-recovery/{email}")
async def recover_password(email: str, db: AsyncSession = Depends(deps.get_db)):
    """
    Password Recovery
    """
    user = await crud.crud_user.get_by_email(db, email=email)

    if user is not None and crud.crud_user.is_admin(user):
        raise HTTPException(
            status_code=404,
            detail="Password recovery for this account is disabled.",
        )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this email does not exist in the system.",
        )
    password_reset_token = generate_password_reset_token(email=email)
    send_reset_password_email(
        email_to=user.email, email=email, token=password_reset_token
    )
    return {"message": "Password recovery email sent"}


@router.post("/reset-password/")
async def reset_password(
    password_reset: schemas.PasswordReset,
    db: AsyncSession = Depends(deps.get_db),
):
    """
    Reset password
    """
    token = password_reset.token
    new_password = password_reset.new_password

    email = verify_password_reset_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")
    user = await crud.crud_user.get_by_email(db, email=email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )

    user_in_data = user.dict()
    user_in_data["password"] = new_password
    user_in_data = schemas.UserUpdate(**user_in_data)

    # Update the password
    updated_user = await crud.crud_user.update(db, db_obj=user, obj_in=user_in_data)
    await crud.crud_user.reset_login_trial(db, db_obj=user)

    return {"message": "Password updated successfully"}
