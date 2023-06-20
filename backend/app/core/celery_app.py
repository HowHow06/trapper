from app.core.config import settings
from celery import Celery
from kombu import Exchange, Queue

# "worker" is the worker name, equilevant to -A
celery_app = Celery("worker", broker=settings.CELERY_BROKER_URL)

# reducing worker_prefetch_multiplier to 1 is an easier and cleaner way to increase the responsiveness of your system without the costs of disabling prefetching entirely.
# https://docs.celeryq.dev/en/stable/userguide/routing.html
celery_app.conf.worker_prefetch_multiplier = 1
celery_app.conf.consumer_timeout = 40

# declared in rabbitmq server using entrypoint script
trapper_default_exchange = Exchange('trapper_fanout_exchange', type='fanout')

celery_app.conf.task_queues = {
    # routing key is ignored because using fanout exhange
    # declared in rabbitmq server using entrypoint script
    # since the queue is declared here, when starting worker, no need to specify -Q
    Queue('trapper-xsstrike', trapper_default_exchange),
}

# celery_app.conf.default_exchange = 'trapper_fanout_exchange'

# since the queue is bound to the fanout exchange, no need to declare task route
celery_app.conf.task_routes = {
    "app.worker.*": {'queue': 'trapper-xsstrike'}
}
