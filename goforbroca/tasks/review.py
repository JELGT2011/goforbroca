from goforbroca.extensions import celery


@celery.task
def review():
    return "OK"
