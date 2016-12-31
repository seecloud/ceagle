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


class FakeApiTestCase(test.TestCase):

    def test_api_response_code(self):
        self.mock_config({
            "use_fake_api_data": True,
        })
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
                    ("", 404), ("unexpected", 404), ("day", 200),
                    ("week", 200), ("month", 200), ("year", 200)):
                urlpath_ = "%s/%s" % (urlpath, suffix)
                code_, resp = self.get(urlpath_)
                self.assertEqual(code, code_, urlpath_)

        for uri in ("unexpected/status/health/day",
                    "unexpected/status/availability/day",
                    "west-1.hooli.net/status/availability/day"):
            uri = "/api/v1/region/" + uri
            code, resp = self.get(uri)
            self.assertEqual(404, code)

    def test_fake_runbooks(self):
        self.mock_config({
            "use_fake_api_data": True,
        })
        region = "region_one"
        runbook_id = "123"
        run_id = "123"
        for uri in ("/api/v1/region/%s/runbooks" % region,
                    "/api/v1/region/%s/runbooks/%s" % (region, runbook_id),
                    "/api/v1/region/%s/runbook_runs" % region,
                    "/api/v1/region/%s/runbook_runs/%s" % (region, run_id)):
            code_, resp = self.get(uri)
            self.assertEqual(200, code_)

        correct_runbook = {
            "name": "test",
            "description": "test",
            "type": "bash",
            "runbook": "echo",
        }
        correct_runbook = json.dumps(correct_runbook)
        incorrect_runbook = json.dumps({})

        # runbooks
        url = "/api/v1/region/%s/runbooks" % region
        code_, resp = self.post(url, data=correct_runbook,
                                content_type='application/json')
        self.assertEqual(201, code_)

        url = "/api/v1/region/%s/runbooks" % region
        code_, resp = self.post(url, data=incorrect_runbook,
                                content_type='application/json')
        self.assertEqual(400, code_)

        # single runbook
        url = "/api/v1/region/%s/runbooks/%s" % (region, runbook_id)
        code_, resp = self.put(url, data=correct_runbook,
                               content_type='application/json')
        self.assertEqual(200, code_)

        url = "/api/v1/region/%s/runbooks/%s" % (region, runbook_id)
        code_, resp = self.put(url, data=incorrect_runbook,
                               content_type='application/json')
        self.assertEqual(400, code_)

        url = "/api/v1/region/%s/runbooks/%s" % (region, runbook_id)
        code_, resp = self.delete(url)
        self.assertEqual(204, code_)

        # run
        url = "/api/v1/region/%s/runbooks/%s/run" % (region, runbook_id)
        code_, resp = self.post(url)
        self.assertEqual(202, code_)
