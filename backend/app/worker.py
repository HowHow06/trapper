import json
import logging
from datetime import datetime

from app import crud, models, scan_task
from app.core.celery_app import celery_app
from app.core.email_util import send_complete_scan_email
from app.db.session import SyncSessionLocal

logger = logging.getLogger("trapper_server")
logger.setLevel(logging.INFO)


@celery_app.task
def test_celery(word: str) -> str:
    print("Hi im test celery worker test!")
    return f"test task return {word}"


@celery_app.task
def perform_scan_celery(scan_request):
    print(f"Worker running....: {scan_request['request_endpoint']}")
    request_package = json.loads(scan_request['original_request_data'])
    scan_task.scan(request_package=request_package,
                   request_id=scan_request['id'])
    return f"test scan return {scan_request['request_endpoint']}"


@celery_app.task
def change_scan_status(task_id, status_id):
    with SyncSessionLocal() as db:
        task = crud.crud_task_sync.get(db=db, id=task_id)
        task_data = task.dict()
        task_data["task_status_id"] = status_id
        task_data["stopped_at"] = datetime.utcnow()

        obj_in = models.Task(**task_data)

        updated_task = crud.crud_task_sync.update(db=db, db_obj=task, obj_in=obj_in)
        send_complete_scan_email(email_to=updated_task.created_by_user.email, task_name=updated_task.task_name, task_id=updated_task.id)
        return f"Change status of task {task_id} to {status_id}"
