from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas
from app.api import deps
# from core.auth import verify_password, create_access_token
from app.models import User as UserModel

router = APIRouter()


@router.post("/testSecured", response_model=schemas.User)
async def read_users_me(current_user: UserModel = Depends(deps.get_current_user)):
    # FastAPI will wait for the get_current_user dependency funciton by default, no need to add await keyword
    return current_user
