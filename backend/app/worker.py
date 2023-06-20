from app.core.celery_app import celery_app
from celery import Celery


@celery_app.task
def test_celery(word: str) -> str:
    print("Hi im test celery worker test!")
    return f"test task return {word}"
