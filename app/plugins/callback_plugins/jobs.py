# -*- coding: utf-8 -*-

from ansible.plugins.callback import CallbackBase


class CallbackModule(CallbackBase):

    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'print'
    CALLBACK_NAME = 'jobs'

    def v2_runner_on_unreachable(self, result):
        print 11111111111
        delegated_vars = result._result.get('_ansible_delegated_vars', None)
        if delegated_vars:
            print "fatal: [%s -> %s]: UNREACHABLE! => %s" % (result._host.get_name(), delegated_vars['ansible_host'], self._dump_results(result._result))
        else:
            print "fatal: [%s]: UNREACHABLE! => %s" % (result._host.get_name(), self._dump_results(result._result)) 
