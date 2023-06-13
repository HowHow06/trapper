from app.api.api_v1.endpoints import auth, healthcheck
from app.api.api_v1.endpoints.secured import testSecured
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(auth.router, tags=["auth"])
api_router.include_router(healthcheck.router, tags=["healthcheck"])
api_router.include_router(testSecured.router, tags=["testSecured"])
# api_router.include_router(users.router, prefix="/users", tags=["users"])
# api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
# api_router.include_router(items.router, prefix="/items", tags=["items"])
