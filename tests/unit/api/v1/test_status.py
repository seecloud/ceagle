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

from tests.unit import test


class ApiTestCase(test.TestCase):

    def test_api_response_code(self):
        region = "north-2.piedpiper.net"
        for urlpath in ("/api/v1/status",
                        "/api/v1/status/performance",
                        "/api/v1/status/availability",
                        "/api/v1/region/%s/status" % region,
                        "/api/v1/region/%s/status/performance" % region,
                        "/api/v1/region/%s/status/availability" % region):
            for suffix, code in (
                    ("", 404), ("unexpected", 404),
                    ("day", 200), ("week", 200), ("month", 200)):
                urlpath_ = "%s/%s" % (urlpath, suffix)
                code_, resp = self.get(urlpath_)
                self.assertEqual(code, code_, urlpath_)

        urlpath = "/api/v1/region/unexpected_region/status/day"
        code, resp = self.get(urlpath)
        self.assertEqual(404, code, urlpath)


@mock.patch("ceagle.config.get_config")
class HealthApiTestCase(test.TestCase):

    def setUp(self):
        super(HealthApiTestCase, self).setUp()
        self.health_config = {"health": {
            "endpoint": "http://dummy.example.org/api/health"
        }}

    @mock.patch("ceagle.api.client.Client")
    def test_status_health_api(self, mock_client, mock_get_config):
        mock_get_config.return_value = self.health_config
        mock_client.return_value.get.return_value = {"status_code": 200}
        code, resp = self.get("/api/v1/status/health/day")
        mock_client.return_value.get.assert_called_with(
            "/api/v1/health", params={"period": u"day"})
        self.assertEqual(200, code)

    @mock.patch("ceagle.api.client.Client")
    def test_region_status_health_api(self, mock_client, mock_get_config):
        mock_get_config.return_value = self.health_config
        mock_client.return_value.get.return_value = {"status_code": 200}

        code, resp = self.get("/api/v1/region/test_region/status/health/day")
        mock_client.return_value.get.assert_called_with(
            "/api/v1/health/test_region", params={"period": u"day"})
        self.assertEqual(200, code)

    def test_health_api_no_endpoint(self, mock_get_config):
        mock_get_config.return_value = {}
        code, resp = self.get("/api/v1/status/health/day")
        self.assertEqual(404, code)
        self.assertEqual({"error": "No health endpoint configured"}, resp)

        code, resp = self.get("/api/v1/region/test_region/status/health/day")
        self.assertEqual(404, code)
        self.assertEqual({"error": "No health endpoint configured"}, resp)
