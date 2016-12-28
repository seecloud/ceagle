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


class FakeApiTestCase(test.TestCase):

    def test_region_api_response_ok(self):
        self.mock_config({"use_fake_api_data": True})
        region = "north-2.piedpiper.net"
        path = "/api/v1/region/%s/infra" % region
        code, resp = self.get(path)
        self.assertEqual(code, 200, path)

    def test_region_api_response_not_found(self):
        self.mock_config({"use_fake_api_data": True})
        path = "/api/v1/region/unexpected_region/infra"
        code, resp = self.get(path)
        self.assertEqual(404, code, path)

    def test_regions_api_response_ok(self):
        self.mock_config({"use_fake_api_data": True})
        path = "/api/v1/infra"
        code, resp = self.get(path)
        self.assertEqual(200, code, path)


class ApiTestCase(test.TestCase):

    def infra(self, name="foo"):
        return {"id": name,
                "title": name.capitalize(),
                "description": "Description for {}.".format(name),
                "urls": [["http://example.org/{}".format(name)]]}

    def test_region_api_response_ok(self):
        foo_infra = [self.infra("foo")]
        self.mock_config({"use_fake_api_data": False,
                          "services": {"infra": {"foo_region": foo_infra}}})
        code, resp = self.get("/api/v1/region/foo_region/infra")
        self.assertEqual(code, 200)
        self.assertEqual(resp, {"infra": foo_infra, "region": "foo_region"})

    def test_region_api_response_not_found(self):
        infra = {"foo_region": [self.infra("foo")]}
        self.mock_config({"use_fake_api_data": False,
                          "services": {"infra": infra}})
        self.assertEqual(self.get("/api/v1/region/bar_region/infra")[0], 404)

    def test_regions_api_response_ok(self):
        infra = {"foo_region": [self.infra("foo")],
                 "bar_region": [self.infra("bar")]}
        self.mock_config({"use_fake_api_data": False,
                          "services": {"infra": infra}})
        code, resp = self.get("/api/v1/infra")
        self.assertEqual(code, 200)
        self.assertEqual({"infra": infra}, resp)

    def test_regions_api_response_not_found(self):
        self.mock_config({"use_fake_api_data": False, "services": {}})
        self.assertEqual(self.get("/api/v1/infra")[0], 404)
