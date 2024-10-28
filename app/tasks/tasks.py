from app.tasks.celery import celery


@celery.task
def send_messages(
    messages: list
):
    pass