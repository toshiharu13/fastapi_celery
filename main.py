import datetime

from fastapi import FastAPI
from celery import Celery

from task import call_background_task

app = FastAPI()

celery = Celery(
    __name__,
    broker='redis://127.0.0.1:6379/0',
    backend='redis://127.0.0.1:6379/0',
    broker_connection_retry_on_startup=True
)


@app.get("/")
async def hello_world(message: str):
    task_datetime = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=10)
    call_background_task.apply_async(args=[message], eta=task_datetime, expires=3600)
    return {'message': 'Hello World!'}
