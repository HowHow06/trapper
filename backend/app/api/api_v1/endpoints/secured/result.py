import json
from datetime import datetime
from typing import Any, List, Optional, Union

from app import crud, models, schemas
from app.api import deps
from app.core import constants, request_util, task_util
from app.models import User as UserModel
from app.worker import change_scan_status, perform_scan_celery
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy import or_
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get("/", response_model=List[schemas.Result])
async def read_results(
    db: AsyncSession = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    sort_by: Optional[str] = None,
    desc_order: bool = False,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve result.
    """
    if crud.crud_user.is_admin(current_user):
        tasks = await crud.crud_result.get_multi(db, skip=skip, limit=limit, sort_by=sort_by, desc_order=desc_order)
    else:
        tasks = await crud.crud_result.get_multi_by_owner(
            db=db,
            created_by_user_id=current_user.id,
            skip=skip,
            limit=limit,
            sort_by=sort_by,
            desc_order=desc_order
        )
    return tasks
