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

from ceagle.api import client
from tests.unit import test  # noqa


class ClientTestCase(test.TestCase):

    def test___init__(self):
        self.assertRaises(TypeError, client.Client)
        self.assertRaises(TypeError, client.Client, "foo")
        self.assertRaises(KeyError, client.Client, "foo", {})
        ct = client.Client("foo", {"endpoint": "foo_ep"})
        self.assertEqual("foo", ct.name)
        self.assertEqual({"endpoint": "foo_ep"}, ct.config)
        self.assertEqual("foo_ep", ct.endpoint)
        self.assertEqual("<Client 'foo'>", repr(ct))

    @mock.patch("ceagle.api.client.requests.get")
    def test_get(self, mock_requests_get):
        mock_requests_get.return_value.status_code = "foo_status"
        mock_requests_get.return_value.json.return_value = (
            {"foo": 42})
        ct = client.Client("foo", {"endpoint": "http://foo_ep"})
        result = ct.get()
        mock_requests_get.assert_called_once_with("http://foo_ep/")
        self.assertEqual({"status_code": "foo_status", "foo": 42}, result)

        mock_requests_get.reset_mock()

        mock_requests_get.return_value.json.return_value = (
            {"foo": 42, "status_code": 24})
        result = ct.get("/bar")
        mock_requests_get.assert_called_once_with("http://foo_ep/bar")
        self.assertEqual({"status_code": 24, "foo": 42}, result)

        mock_requests_get.return_value.json.side_effect = ValueError
        result = ct.get("/bar")
        self.assertEqual(
            {"error": {"message": "Response can not be decoded"},
             "status_code": 500},
            result)

        mock_requests_get.side_effect = (
            client.requests.exceptions.ConnectionError)
        result = ct.get("/bar")
        mesg = "Service 'foo' is not available at 'http://foo_ep'"
        self.assertEqual({"error": {"message": mesg},
                          "status_code": 502},
                         result)


class ModuleTestCase(test.TestCase):

    @mock.patch("ceagle.api.client.config")
    def test_get_config(self, mock_config):
        self.assertRaises(TypeError, client.get_client)
        mock_config.get_config.return_value = {"bar": {}}
        self.assertIsNone(client.get_client("foo"))
        mock_config.get_config.return_value = {"foo": {"endpoint": ""}}
        self.assertIsNone(client.get_client("foo"))

        cfg = {"foo": {"endpoint": "http://foo_ep",
                       "extra_option": 42}}
        mock_config.get_config.return_value = cfg
        ct = client.get_client("foo")
        self.assertIsInstance(ct, client.Client)
        self.assertEqual("foo", ct.name)
        self.assertEqual(cfg["foo"], ct.config)
