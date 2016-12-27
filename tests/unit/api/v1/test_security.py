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

from tests.unit import test

import ddt
import mock


fake_config = mock.Mock()
fake_config.get_config.return_value = {
    "use_fake_api_data": True,
    "services": {
        "security": "ok",
    }
}


@ddt.ddt
@mock.patch("ceagle.api.client.config", fake_config)
class SecurityTestCase(test.TestCase):

    def test_get_issues_all_regions(self):
        resp = self.get("/api/v1/security/issues/week")
        self.assertEqual(200, resp[0])
        self.assertEqual(3, len(resp[1]["issues"]))

    def test_get_issues_month(self):
        resp = self.get("/api/v1/region/region1/security/issues/month")
        self.assertEqual(200, resp[0])
        self.assertEqual(2, len(resp[1]["issues"]))

    def test_get_issues_week(self):
        resp = self.get(
            "/api/v1/region/north-2.piedpiper.net/security/issues/week")
        self.assertEqual(200, resp[0])
        self.assertEqual(2, len(resp[1]["issues"]))

    def test_get_issues_day(self):
        resp = self.get(
            "/api/v1/region/north-2.piedpiper.net/security/issues/day")
        self.assertEqual(200, resp[0])
        self.assertEqual(1, len(resp[1]["issues"]))

    def test_get_issues_empty(self):
        resp = self.get("/api/v1/region/region1/security/issues/day")
        self.assertEqual((200, {"issues": []}), resp)

    def test_get_issues_unknown_region(self):
        resp = self.get("/api/v1/region/region3/security/issues/day")
        self.assertEqual(404, resp[0])

    def test_get_issues_404(self):
        resp = self.get("/api/v1/region/region3/day")
        self.assertEqual(404, resp[0])