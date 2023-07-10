import json
import logging

from app import scan_task
from app.core.celery_app import celery_app

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
    # if status == TaskStatus.WORKING:  # just to change the status, indicate that the task has started
    #     # 更新任务状态和hunter状态
    #     current_task_status = TaskService.get_task_status(task_id=task_id)
    #     if current_task_status and current_task_status < TaskStatus.WORKING:
    #         TaskService.update(
    #             fields=({Task.task_status: TaskStatus.WORKING}), where=(Task.id == task_id))
    #     TaskService.update(
    #         fields=({Task.hunter_status: TaskStatus.WORKING}), where=(Task.id == task_id))
    #     logger.warn("there is a task [task_id:{}, create_user:{}] has start".format(
    #         task_id, create_user))
    # elif status == TaskStatus.KILLED:
    #     try:
    #         TaskService.update(
    #             fields=({Task.hunter_status: TaskStatus.DONE}), where=(Task.id == task_id))
    #         current_task = TaskService.get_fields_by_where(
    #             where=(Task.id == task_id))[0]
    #         if current_task.hunter_status == TaskStatus.DONE and current_task.sqlmap_status == TaskStatus.DONE \
    #                 and current_task.xssfork_status == TaskStatus.DONE:
    #             TaskService.update(
    #                 fields=({Task.task_status: TaskStatus.DONE}), where=(Task.id == task_id))
    #             task_notice_celery.delay(
    #                 message={"type": BroadCastType.TASK, "action": BroadCastAction.COMPLETE_TASK_NOTIFICATION,
    #                          "data": {"task_id": task_id}})

    #     except Exception:
    #         logger.exception("scan_celery error")
    #     logger.warn("there is a task [task_id:{}, create_user:{}] has killed".format(
    #         task_id, create_user))
    # else:  # when the status is NONE
    #     scan(package=package, task_id=task_id,
    #          create_user=create_user, status=status)
