# -*- coding: utf8 -*-

from ansible.inventory import Inventory
from ansible.inventory.host import Host as Inv_Host
from ansible.inventory.group import Group as Inv_Group
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager

from . import db
from models import Host, Group, groups_hosts, groups_groups


def get_inventory():
    loader = DataLoader()
    variable_manager = VariableManager()
    inventory = Inventory(loader=loader,
                          variable_manager=variable_manager,
                          host_list=None)
    # Add all host to 'all' group and ungrouped host to 'ungrouped' group.
    ungrouped = inventory.get_group('ungrouped')
    all = inventory.get_group('all')

    hosts = Host.query.all()
    for host in hosts:
        inv_host = Inv_Host(name=host.name)
        inv_host.set_variable('ansible_host', host.host)
        inv_host.set_variable('ansible_port', host.port)
        inv_host.set_variable('ansible_user', host.user)
        all.add_host(inv_host)

        if host.groups:
            for group in host.groups:
                if group.name not in inventory.get_groups().keys():
                    inv_group = Inv_Group(name=group.name)
                    inventory.add_group(inv_group)
                else:
                    inv_group = inventory.get_group(group.name)
                inv_group.add_host(inv_host)
        else:
            ungrouped.add_host(inv_host)
    return inventory
