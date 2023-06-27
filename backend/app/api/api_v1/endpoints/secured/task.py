from datetime import datetime
from typing import Any, List

from app import crud, models, schemas
from app.api import deps
from app.core import constants
from app.models import User as UserModel
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get("/", response_model=List[schemas.Task])
async def read_tasks(
    db: AsyncSession = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve tasks.
    """
    if crud.crud_user.is_admin(current_user):
        tasks = await crud.crud_task.get_multi(db, skip=skip, limit=limit)
    else:
        tasks = await crud.crud_task.get_multi_by_owner(
            db=db, created_by_user_id=current_user.id, skip=skip, limit=limit
        )
    return tasks


@router.post("/", response_model=schemas.Task)
async def create_task(
    *,
    db: AsyncSession = Depends(deps.get_db),
    task_in: schemas.TaskCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new task.
    """
    task = await crud.crud_task.create_with_owner(
        db=db, obj_in=task_in, created_by_user_id=current_user.id)
    return task


@router.put("/{id}", response_model=schemas.Task)
async def update_task(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: int,
    task_in: schemas.TaskUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an task.
    """
    task = await crud.crud_task.get(db=db, id=id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if (not crud.crud_user.is_admin(current_user)) and (task.created_by_user_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    task = await crud.crud_task.update(db=db, db_obj=task, obj_in=task_in)
    return task


@router.get("/{id}", response_model=schemas.Task)
async def read_task(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get task by ID.
    """
    task = await crud.crud_task.get(db=db, id=id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if (not crud.crud_user.is_admin(current_user)) and (task.created_by_user_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return task


@router.delete("/{id}", response_model=schemas.Task)
async def delete_task(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an task.
    """
    task = await crud.crud_task.get(db=db, id=id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if (not crud.crud_user.is_admin(current_user)) and (task.created_by_user_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    task = await crud.crud_task.remove(db=db, id=id)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "Operation successful. Task has been deleted.",
            "id": id
        },
    )


@router.post("/{id}/start-task")
async def start_task(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Start an task.
    """
    task = await crud.crud_task.get(db=db, id=id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if (not crud.crud_user.is_admin(current_user)) and (task.created_by_user_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")

    if task.task_status_id in [constants.Status.RUNNING]:
        raise HTTPException(
            status_code=400, detail="Operation failed. Task is already started.")
    if task.task_status_id in [constants.Status.KILLED, constants.Status.DONE]:
        raise HTTPException(
            status_code=400, detail="Operation failed. Task is already stopped.")

    task_data = jsonable_encoder(task)
    task_data["task_status_id"] = constants.Status.RUNNING

    obj_in = models.Task(**task_data)

    await crud.crud_task.update(db=db, db_obj=task, obj_in=obj_in)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "Operation successful. Task has been started."
        },
    )


@router.post("/{id}/stop-task")
async def stop_task(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Stop an task.
    """
    task = await crud.crud_task.get(db=db, id=id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if (not crud.crud_user.is_admin(current_user)) and (task.created_by_user_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")

    if task.task_status_id in [constants.Status.DONE, constants.Status.KILLED]:
        raise HTTPException(
            status_code=400, detail="Operation failed. Task is already stopped.")

    task_data = jsonable_encoder(task)
    # will turn to DONE when celery stopped, or last scan request stopped
    task_data["task_status_id"] = constants.Status.KILLED
    task_data["stopped_at"] = datetime.utcnow()

    obj_in = models.Task(**task_data)

    # TODO: stop celery here

    await crud.crud_task.update(db=db, db_obj=task, obj_in=obj_in)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "Operation successful. Task has been stopped."
        },
    )
