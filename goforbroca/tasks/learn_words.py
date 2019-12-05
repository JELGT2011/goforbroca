from datetime import datetime

from goforbroca.extensions import celery
from goforbroca.models.courses import Courses
from goforbroca.models.repetitions import Repetitions


@celery.task
def learn_words():
    courses = Courses.all()
    now = datetime.utcnow()
    for course in courses:
        target = course.words_per_week
        current = Repetitions.new_words_this_week(course.id)
    return "OK"
