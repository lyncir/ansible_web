# -*- coding: utf-8 -*-
import time
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.playbook import Playbook
from ansible.executor.playbook_executor import PlaybookExecutor
from mock import MagicMock

#from . import celery
from utils import get_inventory


#@celery.task()
def add(a, b):
    return a + b


def test():
    loader = DataLoader()
    variable_manager = VariableManager()
    inventory = get_inventory()
    print inventory.get_hosts()
    options = MagicMock()

    playbook = PlaybookExecutor(playbooks=['app/test.yml'],
                                inventory=inventory,
                                variable_manager=variable_manager,
                                loader=loader,
                                options=options,
                                passwords=[])
    result = playbook.run()
    print result
