from app.api.api_v1.endpoints import auth, test
from app.api.api_v1.endpoints.secured import test_secured
from app.core.config import settings
from fastapi import APIRouter

api_router = APIRouter()
# tags are for openapi document
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

# api_router.include_router(users.router, prefix="/users", tags=["users"])
# api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
# api_router.include_router(items.router, prefix="/items", tags=["items"])

if settings.ENVIRONMENT == "dev":
    api_router.include_router(test.router, tags=["test"])
    api_router.include_router(test_secured.router, tags=["test-secured"])
