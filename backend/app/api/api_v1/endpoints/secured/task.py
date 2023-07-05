from datetime import datetime
from typing import Any, List, Optional, Union

from app import crud, models, schemas
from app.api import deps
from app.core import constants, utils
from app.models import User as UserModel
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy import or_
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get("/", response_model=List[schemas.Task])
async def read_tasks(
    db: AsyncSession = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    sort_by: Optional[str] = None,
    desc_order: bool = False,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve tasks.
    """
    if crud.crud_user.is_admin(current_user):
        tasks = await crud.crud_task.get_multi(db, skip=skip, limit=limit, sort_by=sort_by, desc_order=desc_order)
    else:
        tasks = await crud.crud_task.get_multi_by_owner(
            db=db,
            created_by_user_id=current_user.id,
            skip=skip,
            limit=limit,
            sort_by=sort_by,
            desc_order=desc_order
        )
    return tasks


@router.get("/current")
async def read_current_task(
    db: AsyncSession = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Union[schemas.Task, None]:
    """
    Retrieve current task for the user.
    """
    condition = or_(models.Task.task_status_id == constants.Status.WAITING,
                    models.Task.task_status_id == constants.Status.RUNNING)
    tasks = await crud.crud_task.get_multi_by_owner(
        db=db,
        created_by_user_id=current_user.id,
        skip=0,
        limit=1,
        sort_by="created_at",
        desc_order=True,
        where=condition
    )

    if tasks and len(tasks) > 0:
        return tasks[0]
    else:
        return None


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
    # Check for current task
    current_task = await read_current_task(db=db, current_user=current_user)
    if current_task is not None:
        raise HTTPException(
            status_code=400,
            detail="Operation failed. User already has a current task, please stop the task before creating a new one."
        )
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
        raise HTTPException(status_code=404, detail="Task not found.")
    if task.task_status_id == constants.Status.RUNNING:
        raise HTTPException(
            status_code=404, detail="Operation failed. The task is running.")
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


@router.post("/{id}/scan-request", response_model=schemas.ScanRequest)
async def create_scan_request(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: int,
    scan_request_in: schemas.ScanRequestCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new scan request.
    """
    try:
        user_id, task_id = utils.decipher_task_access_key(
            scan_request_in.task_access_key)
    except:
        raise HTTPException(
            status_code=400, detail="Invalid access key.")

    if task_id != id:
        raise HTTPException(
            status_code=400, detail="Operation failed. Invalid access key.")

    task = await crud.crud_task.get(db=db, id=id)

    is_given_task_id_not_aligned = task_id != task.id
    is_not_same_user = task.created_by_user_id != user_id
    is_not_current_user = task.created_by_user_id != current_user.id and not (crud.crud_user.is_admin(
        current_user))
    is_task_running = task.task_status_id == constants.Status.RUNNING

    if is_given_task_id_not_aligned or is_not_same_user or is_not_current_user:
        raise HTTPException(
            status_code=400, detail="Operation failed. Invalid access key.")

    if not is_task_running:
        raise HTTPException(
            status_code=400, detail="Operation failed. Task is not running.")

    scan_request_data = jsonable_encoder(scan_request_in)
    scan_request_data["task_id"] = task_id
    scan_request_data["scan_status_id"] = constants.Status.WAITING
    # TODO: get the information by analyzing the package
    scan_request_data["request_endpoint"] = "PENDING CHANGE LOGIC"
    scan_request_data["request_information"] = "PENDING CHANGE LOGIC"
    scan_request_data["request_hash"] = "PENDING CHANGE LOGIC"

    obj_in = models.ScanRequest(**scan_request_data)

    scan_request = await crud.crud_scan_request.create(
        db=db, obj_in=obj_in)

    # TODO: start celery app scan here
    return scan_request
