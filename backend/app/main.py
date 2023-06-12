from fastapi import FastAPI
# from starlette.middleware.cors import CORSMiddleware
from app.api.api_v1.api import api_router
from app.core.config import settings

app = FastAPI(
    title=settings.API_SERVER_PROJECT_NAME, openapi_url=f"{settings.API_PREFIX}/openapi.json"
)

# # Set all CORS enabled origins
# if settings.BACKEND_CORS_ORIGINS:
#     app.add_middleware(
#         CORSMiddleware,
#         allow_origins=[str(origin)
#                        for origin in settings.BACKEND_CORS_ORIGINS],
#         allow_credentials=True,
#         allow_methods=["*"],
#         allow_headers=["*"],
#     )


@app.get("/")
def read_root():
    return {"Hello": "Worldo"}


app.include_router(api_router, prefix=settings.API_PREFIX)
