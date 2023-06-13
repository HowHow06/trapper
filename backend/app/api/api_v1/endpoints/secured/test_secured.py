from app import schemas
from app.api import deps
from app.models import User as UserModel
from fastapi import APIRouter, Depends

router = APIRouter()


@router.post("/test-secured-user", response_model=schemas.User)
async def test_secured_active_user(current_user: UserModel = Depends(deps.get_current_active_user)):
    # FastAPI will wait for the get_current_user dependency funciton by default, no need to add await keyword
    return current_user


@router.post("/test-secured-admin", response_model=schemas.User)
async def test_secured_active_admin(current_admin: UserModel = Depends(deps.get_current_active_admin)):
    return current_admin
