from typing import Any

from app.api import deps
from app.core.celery_app import celery_app
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import OperationalError
from sqlmodel.ext.asyncio.session import AsyncSession

router = APIRouter()


@router.get("/test/healthcheck-db")
async def healthcheck_db(db: AsyncSession = Depends(deps.get_db)):
    try:
        # Try to query for an arbitrary table
        await db.execute("SELECT 1")
        return {"status": "ok"}
    except OperationalError:
        raise HTTPException(
            status_code=500, detail="Cannot connect to the database")


@router.post("/test/test-celery", status_code=201)
def test_celery(msg: str) -> Any:
    """
    Test Celery worker.
    """
    # celery_app.test_celery.delay(msg.msg)
    celery_app.send_task("app.worker.test_celery", args=[msg])
    return {"msg": "Word received"}
