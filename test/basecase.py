# Copyright (c) 2017-2018, Intel Corporation
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#    * Redistributions of source code must retain the above copyright notice,
#      this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of Intel Corporation nor the names of its contributors
#      may be used to endorse or promote products derived from this software
#      without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os

import unittest
import test.config as config

from iotkitclient import Client

USERNAME = "testuser"
PASSWORD = "P@ssw0rd"
ROLE = "admin"


class BaseCase(unittest.TestCase):
    """ Test case that creates a connection to server as
        configured in config.py in test directory. """

    def setUp(self):
        self.client = Client(config.api_url)
        self.client.auth(config.username, config.password)

    def tearDown(self):
        print("Resetting DB")
        os.system("docker exec -it {} node /app/admin "
                  "resetDB &> /dev/null".format(config.dashboard_container))
        os.system("docker exec -it {} node /app/admin addUser {} {} {} "
                  "&> /dev/null".format(config.dashboard_container,
                                        config.username,
                                        config.password,
                                        config.role))


class BaseCaseWithAccount(BaseCase):
    """ Test case that has an account."""

    def setUp(self):
        BaseCase.setUp(self)
        self.account = self.client.create_account(config.accountname)
        # Reauth to access new Account
        self.client.auth(config.username, config.password)
