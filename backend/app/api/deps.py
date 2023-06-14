from typing import Generator

import jwt
from app import schemas
from app.core import auth as AuthHelper
from app.core.config import settings
from app.core.utils import OAuth2PasswordBearerWithCookie
from app.crud import crud_user
from app.db.session import AsyncSessionLocal
from app.models import user as UserModel
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_PREFIX}/login")
oauth2_scheme = OAuth2PasswordBearerWithCookie(
    tokenUrl=f"{settings.API_PREFIX}/auth/login")


async def get_db() -> Generator:
    # async with AsyncSessionLocal() as session:
    #     yield session
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()


async def get_current_user(db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)) -> UserModel:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.ACCESS_TOKEN_SECRET_KEY,
                             algorithms=[AuthHelper.ALGORITHM])
        # **payload is used to unpack the payload dictionary and pass its key-value pairs as keyword arguments to the constructor.
        token_data = schemas.TokenPayload(**payload)
    except (jwt.PyJWTError, ValidationError) as error:
        print(error)
        raise credentials_exception
    user_id = token_data.sub
    user = await crud_user.get(db, id=user_id)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: UserModel = Depends(get_current_user),
) -> UserModel:
    if not crud_user.is_active(current_user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user


async def get_current_active_admin(
    current_user: UserModel = Depends(get_current_active_user),
) -> UserModel:
    if not crud_user.is_admin(current_user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="The user doesn't have enough privileges"
        )
    return current_user
