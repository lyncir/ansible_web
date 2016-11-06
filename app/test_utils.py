# -*- coding: utf-8 -*-

import pytest
from assertpy import assert_that

from app.utils import Runner


def run(playbooks, run_data, private_key_file, password, verbosity):
    runner = Runner(
        playbooks=playbooks,
        run_data=run_data,
        private_key_file=private_key_file,
        password=password,
        verbosity=verbosity)
    status = runner.run()

    assert_that(status).is_equal_to(0)


def test_runner():
    playbooks = ['test']
    verbosity = 0

    # Use key file, no sudo
    private_key_file = 'keyfilename'
    password = None
    run_data = {"host": "dev", "user": "testaccount", "become": 'no'}
    run(playbooks, run_data, private_key_file, password, verbosity)

    # Use key file, sudo, must be password
    private_key_file = 'keyfilename'
    password = 'password'
    run_data = {"host": "dev", "user": "testaccount", "become": 'yes'}
    run(playbooks, run_data, private_key_file, password, verbosity)

    # Use password, no sudo
    private_key_file = None
    password = 'password'
    run_data = {"host": "dev", "user": "testaccount", "become": 'no'}
    run(playbooks, run_data, private_key_file, password, verbosity)

    # Use password, sudo
    private_key_file = None
    password = 'password'
    run_data = {"host": "dev", "user": "testaccount", "become": 'yes'}
    run(playbooks, run_data, private_key_file, password, verbosity)

