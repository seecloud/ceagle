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


import json

from tests.unit import test


class AppTestCase(test.TestCase):

    def test_cloud_status(self):
        rv = self.app.get("/cloud_status/v1/")
        self.assertEqual(200, rv.status_code)
        res = json.loads(rv.data.decode())
        self.assertIn("region_names", res)
        self.assertIn("regions", res)

    def test_cloud_status_health(self):
        rv = self.app.get("/cloud_status/health/v1")
        self.assertEqual(200, rv.status_code)
        res = json.loads(rv.data.decode())
        self.assertIn("project_names", res)
        self.assertIn("projects", res)

    def test_cloud_status_availability(self):
        rv = self.app.get("/cloud_status/availability/v1")
        self.assertEqual(200, rv.status_code)
        res = json.loads(rv.data.decode())
        self.assertIn("project_names", res)
        self.assertIn("projects", res)

    def test_not_found(self):
        rv = self.app.get("/unexisting/path/to/somewhere/else")
        self.assertEqual(404, rv.status_code)
        res = json.loads(rv.data.decode())
        self.assertEqual({"error": "Not found"}, res)
