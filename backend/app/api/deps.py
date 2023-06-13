from typing import Generator

import jwt
from app import schemas
from app.core import auth as AuthHelper
from app.core.config import settings
from app.crud import crud_user
from app.db.session import AsyncSessionLocal
from app.models import user as UserModel
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_PREFIX}/login")


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
    except (jwt.JWTError, ValidationError):
        raise credentials_exception
    user_id = token_data.sub
    user = await crud_user.get(db, id=user_id)
    if user is None:
        raise credentials_exception
    return user


# def get_current_active_user(
#     current_user: models.User = Depends(get_current_user),
# ) -> models.User:
#     if not crud.user.is_active(current_user):
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user


# def get_current_active_superuser(
#     current_user: models.User = Depends(get_current_user),
# ) -> models.User:
#     if not crud.user.is_superuser(current_user):
#         raise HTTPException(
#             status_code=400, detail="The user doesn't have enough privileges"
#         )
#     return current_user
