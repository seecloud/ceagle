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

import collections

import mock

from tests.unit import test


class ApiTestCase(test.TestCase):

    def test_api_response_code(self):
        self.mock_config({
            "use_fake_api_data": False,
        })
        code, resp = self.get("/api/v1/regions")
        self.assertEqual(code, 200)
        code, resp = self.get("/api/v1/regions/detailed")
        self.assertEqual(code, 200)


class RegionsApiTestCase(test.TestCase):

    def setUp(self):
        super(RegionsApiTestCase, self).setUp()
        self.mock_config({
            "use_fake_api_data": False,
        })
        self.mock_services(collections.OrderedDict([
            ("availability", "foo_endpoint"),
            ("health", "foo_endpoint"),
            ("infra", {}),
        ]))

    def mock_services(self, services):
        patch = mock.patch.dict("oss_lib.config._CONF", {
            "services": services,
        })
        patch.start()
        self.addCleanup(patch.stop)

    @mock.patch("ceagle.api.client.get_client")
    def test_get_regions(self, mock_get_client):
        mock_get_client.return_value.get.side_effect = [
            (["a1", "b1", "c1"], 200),
            (["b1", "d1", "e1"], 200),
        ]
        code, resp = self.get("/api/v1/regions")
        self.assertEqual(200, code)
        resp["regions"].sort()
        self.assertEqual({"regions": ["a1", "b1", "c1", "d1", "e1"]}, resp)

    @mock.patch("ceagle.api.client.get_client")
    def test_get_resions_detailed(self, mock_get_client):
        mock_get_client.return_value.get.side_effect = [
            (["a2", "b2", "c2"], 200),
            (["b2", "d2", "e2"], 200),
        ]
        code, resp = self.get("/api/v1/regions/detailed")
        self.assertEqual(200, code)
        self.assertEqual({
            "regions": {
                "a2": {"services": ["availability"]},
                "b2": {"services": ["availability", "health"]},
                "c2": {"services": ["availability"]},
                "d2": {"services": ["health"]},
                "e2": {"services": ["health"]}
            }
        }, resp)
