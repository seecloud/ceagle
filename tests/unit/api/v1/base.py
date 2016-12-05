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

from ceagle.api_fake_data import base as fake_api_base
from tests.unit import test


class ApiTestCase(test.TestCase):

    def setUp(self):
        super(ApiTestCase, self).setUp()
        self.old_USE_FAKE_DATA = fake_api_base.USE_FAKE_DATA
        fake_api_base.USE_FAKE_DATA = False

    def tearDown(self):
        fake_api_base.USE_FAKE_DATA = self.old_USE_FAKE_DATA
        super(ApiTestCase, self).tearDown()
