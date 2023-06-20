from app.core.config import settings
from celery import Celery
from kombu import Exchange, Queue

# "worker" is the worker name, equilevant to -A
celery_app = Celery("worker", broker=settings.CELERY_BROKER_URL)

# reducing worker_prefetch_multiplier to 1 is an easier and cleaner way to increase the responsiveness of your system without the costs of disabling prefetching entirely.
# https://docs.celeryq.dev/en/stable/userguide/routing.html
celery_app.conf.worker_prefetch_multiplier = 1
celery_app.conf.consumer_timeout = 40
celery_app.conf.task_serializer = 'json'
celery_app.conf.result_serializer = 'json'
celery_app.conf.accept_content = ['json']
celery_app.conf.timezone = 'UTC'
celery_app.conf.enable_utc = True
# If task_acks_late is set to True, tasks will be acknowledged after they have been executed, not just when they have been received.
# This means that if a worker crashes while executing a task, the task will be returned to the queue and can be picked up by another worker.
celery_app.conf.task_acks_late = True

# declared in rabbitmq server using entrypoint script
trapper_default_exchange = Exchange('trapper_fanout_exchange', type='fanout')

celery_app.conf.task_queues = {
    # routing key is ignored because using fanout exhange
    # declared in rabbitmq server using entrypoint script
    # since the queue is declared here, when starting worker, no need to specify -Q
    Queue('trapper-xsstrike', trapper_default_exchange),
}

# since the queue is bound to the fanout exchange,
# the same message will also be sent to any queue bound to the same exchange
celery_app.conf.task_routes = {
    "app.worker.*": {'queue': 'trapper-xsstrike'}
}
