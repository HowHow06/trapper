from datetime import datetime
from typing import Any, List, Optional

from app import crud, models, schemas
from app.api import deps
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get("/", response_model=List[schemas.ScanRequest])
async def read_scan_requests(
    db: AsyncSession = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    sort_by: Optional[str] = None,
    desc_order: bool = False,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve scan requests.
    """
    if crud.crud_user.is_admin(current_user):
        requests = await crud.crud_scan_request.get_multi(db, skip=skip, limit=limit, sort_by=sort_by, desc_order=desc_order)
    else:
        requests = await crud.crud_scan_request.get_multi_by_owner(
            db=db,
            created_by_user_id=current_user.id,
            skip=skip,
            limit=limit,
            sort_by=sort_by,
            desc_order=desc_order
        )
    return requests
