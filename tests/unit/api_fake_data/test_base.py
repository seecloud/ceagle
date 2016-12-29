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

import mock

from ceagle.api_fake_data import base
from tests.unit import test


class ModuleTestCase(test.TestCase):

    @mock.patch("ceagle.api_fake_data.base.config")
    def test_api_handler(self, mock_config):
        mock_config.get_config.return_value = {}
        fake = lambda: "fake"
        real = lambda: "real"
        self.assertEqual("fake", base.api_handler(fake)(real)())
        self.assertEqual(base.USE_FAKE_DATA, True)
        base.USE_FAKE_DATA = False
        self.assertEqual("real", base.api_handler(fake)(real)())

    @mock.patch("ceagle.api_fake_data.base.random")
    def test_randnum(self, mock_random):
        mock_random.random.return_value = 42.4242
        self.assertEqual(3828.178, base.randnum(10, 100, 5))
        self.assertEqual(3828.18, base.randnum(10, 100))
        self.assertEqual(3828.2, base.randnum(10, 100, 1))
        self.assertEqual([mock.call()] * 3, mock_random.random.mock_calls)


class FakeClientTestCase(test.TestCase):

    def test_default(self):
        c = base.FakeClient("name", "endpoint")
        res = c.get("/none")
        self.assertEqual(404, res[1])


class GenerateDataTestCase(test.TestCase):

    def test_gen(self):
        def gen(ts):
            return "sample data for %s" % ts
        gen = base.generate_data("day", gen)
        for i in gen:
            print i
        self.assertEqual(1, 2)
