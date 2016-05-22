# -*- coding: utf-8 -*-

from . import celery
from utils import Runner


@celery.task()
def add(a, b):
    return a + b


@celery.task()
def deploy(playbooks, run_data, private_key_file=None, password=None, verbosity=0):
    runner = Runner(
            playbooks=playbooks,
            run_data=run_data,
            private_key_file=private_key_file,
            password=password,
            verbosity=verbosity)
    print runner.run()
