# -*- coding: utf-8 -*-
import time

from . import celery
from utils import Runner


@celery.task()
def add(a, b):
    return a + b


@celery.task()
def test():
    run_data = {'host': 'all', 'user': 'user'}
    passwords = {'conn_pass': 'password', 'become_pass': 'passowrd'}
    runner = Runner(
            playbooks=['test'],
            run_data=run_data,
            passwords=passwords,
            verbosity=3)
    print runner.run()
