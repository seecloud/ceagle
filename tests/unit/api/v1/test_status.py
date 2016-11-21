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


class ApiTestCase(test.TestCase):

    def test_api_response_code(self):
        region = "north-2.piedpiper.net"
        for urlpath in ("/api/v1/status",
                        "/api/v1/status/health",
                        "/api/v1/status/performance",
                        "/api/v1/status/availability",
                        "/api/v1/region/%s/status" % region,
                        "/api/v1/region/%s/status/health" % region,
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
