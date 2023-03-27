import os
from celery import Celery
from calculation import calculate
import logging


RESOURCE_SCREENING_INTERVAL = 30

REDIS_ADDR = os.environ.get('REDIS_ADDR')
celeryapp = Celery('task_scheduler', backend=REDIS_ADDR, broker=REDIS_ADDR)

logging.basicConfig(filename='myapp.log', level=logging.INFO)


@celeryapp.task(name='schedule')
def start_calc_deploy(job):
    scheduling_result = calculate(job)  # scheduling_result can be a node object
    return scheduling_result


@celeryapp.task(name='test')
def test_celery():
    return "ok"
