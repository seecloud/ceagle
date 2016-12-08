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
        ct = client.Client("foo", "foo_ep")
        self.assertEqual("foo", ct.name)
        self.assertEqual("foo_ep", ct.endpoint)
        self.assertEqual("<Client 'foo'>", repr(ct))

    @mock.patch("ceagle.api.client.requests.get")
    def test_get(self, mock_requests_get):
        mock_requests_get.return_value.status_code = "foo_status"
        mock_requests_get.return_value.json.return_value = {"foo": 42}
        ct = client.Client("foo", "http://foo_ep")
        result = ct.get()
        mock_requests_get.assert_called_once_with("http://foo_ep/")
        self.assertEqual(({"foo": 42}, "foo_status"), result)

        mock_requests_get.reset_mock()

    @mock.patch("ceagle.api.client.requests.get")
    def test_get_with_path(self, mock_requests_get):
        mock_requests_get.return_value.json.return_value = {"foo": 42}
        mock_requests_get.return_value.status_code = 200
        ct = client.Client("foo", "http://foo_ep")
        result = ct.get("/bar")
        mock_requests_get.assert_called_once_with("http://foo_ep/bar")
        self.assertEqual(({"foo": 42}, 200), result)

    @mock.patch("ceagle.api.client.requests.get")
    def test_get_wrong_response_fmt(self, mock_requests_get):
        mock_requests_get.return_value.json.side_effect = ValueError
        ct = client.Client("foo", "http://foo_ep")
        result = ct.get("/bar")
        self.assertEqual(
            ({"error": {"message": "Response can not be decoded"}}, 500),
            result)

    @mock.patch("ceagle.api.client.requests.get")
    def test_get_not_available(self, mock_requests_get):
        mock_requests_get.side_effect = (
            client.requests.exceptions.ConnectionError)
        ct = client.Client("foo", "http://foo_ep")
        result = ct.get("/bar")
        mesg = "Service 'foo' is not available at 'http://foo_ep'"
        self.assertEqual(({"error": {"message": mesg}}, 502),
                         result)


class ModuleTestCase(test.TestCase):

    @mock.patch("ceagle.api.client.config")
    def test_get_config(self, mock_config):
        self.assertRaises(TypeError, client.get_client)
        mock_config.get_config.return_value = {"services": {"bar": {}}}
        self.assertRaises(client.UnknownService, client.get_client, "foo")
        mock_config.get_config.return_value = {"services": {"foo": ""}}
        self.assertRaises(client.UnknownService, client.get_client, "foo")

        cfg = {"services": {"foo": "http://foo_ep"}}
        mock_config.get_config.return_value = cfg
        ct = client.get_client("foo")
        self.assertIsInstance(ct, client.Client)
        self.assertEqual("foo", ct.name)
        self.assertEqual(cfg["services"]["foo"], ct.endpoint)
