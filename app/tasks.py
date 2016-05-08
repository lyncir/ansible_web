# -*- coding: utf-8 -*-
import time

from . import celery
from utils import Runner


@celery.task()
def add(a, b):
    return a + b


@celery.task()
def test():
    run_data = {'host': 'dev', 'user': 'root'}
    runner = Runner(
            playbooks=['test'],
            run_data=run_data,
            private_key_file='key_name',
            #password=password,
            password=None,
            verbosity=3)
    print runner.run()
