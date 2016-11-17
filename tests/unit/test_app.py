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


class AppTestCase(test.TestCase):

    def test_cloud_status(self):
        code, resp = self.get("/api/v1/cloud_status/")
        self.assertEqual(200, code)
        self.assertIn("regions", resp)

    def test_cloud_status_health(self):
        code, resp = self.get("/api/v1/cloud_status/health/")
        self.assertEqual(200, code)
        self.assertIn("project_names", resp)

    def test_cloud_status_availability(self):
        code, resp = self.get("/api/v1/cloud_status/availability/")
        self.assertEqual(200, code)
        self.assertIn("project_names", resp)

    def test_not_found(self):
        code, resp = self.get("/unexisting/path/to/somewhere/else")
        self.assertEqual(404, code)
        self.assertEqual({"error": "Not Found"}, resp)

    def test_api_map(self):
        code, resp = self.get("/api/v1")
        self.assertEqual(200, code)
        part = {"endpoint": "capacity.index",
                "methods": ["GET", "HEAD", "OPTIONS"],
                "uri": "/api/v1/capacity/"}
        self.assertIn(part, resp)
