# -*- coding: utf-8 -*-
import time
from . import celery


@celery.task()
def add(a, b):
    return a + b
