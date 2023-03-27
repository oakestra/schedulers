import sys, os
import csv
import time
from unittest.mock import MagicMock
import random
import calculation

results = [["test_n", "component", "overhead", "setup"]]


def gen_resources(num):
    random.seed(time.time())
    resources = []
    for i in range(num):
        resources.append({
            'id': 'id-' + str(i),
            'name': 'name-' + str(i),
            'available_cpu': i,
            'available_memory': 100 + i,
            'virtualization': ['container']
        })
    return resources


def test_benchmark():
    calculation.get_available_resources = MagicMock(return_value=gen_resources(45))
    job = {
        'job_id': 'myjob-1',
        'requirements': {
            "vcpu": 2,
            "memory": 102,
            "virtualization": "container"
        },
    }

    res = calculation.calculate(job)
    res = res['results']

    assert len(res) == 43
    assert res[0] == 'id-44'
