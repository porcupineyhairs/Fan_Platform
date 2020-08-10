from App import create_app
from App.celery_ import create_celery
celery = create_celery(create_app())


@celery.task(name="tasks.add_together")
def add_together(a, b):
    return a + b