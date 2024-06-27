# -*- coding: utf-8 -*-
# zato: ide-deploy=True

from zato.server.service import Service


class test_server(Service):
    name = 'sigdep.test.server'

    def handle(self):
        self.response.payload = {'response': 'OK'}
