from goforbroca.extensions import celery
from goforbroca.models.courses import Courses


@celery.task
def retain_words():
    courses = Courses.all()
    for course in courses:
        pass
    return "OK"
