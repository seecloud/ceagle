# Copyright 2016: Mirantis Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import copy
import json

import mock
from oss_lib import config
import testtools

from ceagle import app
from ceagle import config as cfg


class TestCase(testtools.TestCase):

    def setUp(self):
        super(TestCase, self).setUp()
        self.addCleanup(mock.patch.stopall)

        app.app.config["TESTING"] = True
        self.app = app.app.test_client()

    def mock_config(self, update=None):
        patch = mock.patch("oss_lib.config._CONF")
        patch.start()
        self.addCleanup(patch.stop)

        defaults = copy.deepcopy(cfg.DEFAULT)
        if update:
            config.merge_dicts(defaults, update)
        config.setup_config(
            defaults=defaults,
            validation_schema=cfg.SCHEMA,
        )

    def get(self, *args, **kwargs):
        rv = self.app.get(*args, **kwargs)
        return rv.status_code, json.loads(rv.data.decode())
