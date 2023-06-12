from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import OperationalError
from sqlmodel.ext.asyncio.session import AsyncSession


from app.api import deps


router = APIRouter()


@router.get("/healthcheck/db")
async def healthcheck_db(db: AsyncSession = Depends(deps.get_db)):
    try:
        # Try to query for an arbitrary table
        await db.execute("SELECT 1")
        return {"status": "ok"}
    except OperationalError:
        raise HTTPException(
            status_code=500, detail="Cannot connect to the database")
