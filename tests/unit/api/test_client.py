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

    @mock.patch("ceagle.api.client.requests.request")
    def test_get(self, mock_requests):
        mock_requests.return_value.status_code = "foo_status"
        mock_requests.return_value.json.return_value = {"foo": 42}
        ct = client.Client("foo", "http://foo_ep")
        result = ct.get()
        mock_requests.assert_called_once_with("GET", "http://foo_ep/")
        self.assertEqual(({"foo": 42}, "foo_status"), result)

    @mock.patch("ceagle.api.client.requests.request")
    def test_get_with_path(self, mock_requests):
        mock_requests.return_value.json.return_value = {"foo": 42}
        mock_requests.return_value.status_code = 200
        ct = client.Client("foo", "http://foo_ep")
        result = ct.get("/bar")
        mock_requests.assert_called_once_with("GET", "http://foo_ep/bar")
        self.assertEqual(({"foo": 42}, 200), result)

    @mock.patch("ceagle.api.client.requests.request")
    def test_get_no_content(self, mock_requests):
        mock_requests.return_value.json.return_value = {"foo": 42}
        mock_requests.return_value.status_code = 204
        ct = client.Client("foo", "http://foo_ep")
        result = ct.get("/bar")
        mock_requests.assert_called_once_with("GET", "http://foo_ep/bar")
        self.assertEqual(("", 204), result)

    @mock.patch("ceagle.api.client.requests.request")
    def test_get_wrong_response_fmt(self, mock_requests):
        mock_requests.return_value.json.side_effect = ValueError
        ct = client.Client("foo", "http://foo_ep")
        result = ct.get("/bar")
        self.assertEqual(
            ({"error": {"message": "Response can not be decoded"}}, 500),
            result)

    @mock.patch("ceagle.api.client.requests.request")
    def test_get_not_available(self, mock_requests):
        mock_requests.side_effect = (
            client.requests.exceptions.ConnectionError)
        ct = client.Client("foo", "http://foo_ep")
        result = ct.get("/bar")
        mesg = "Service 'foo' is not available at 'http://foo_ep'"
        self.assertEqual(({"error": {"message": mesg}}, 502),
                         result)

    @mock.patch("ceagle.api.client.requests.request")
    def test_methods(self, mock_requests):
        mock_requests.return_value.json.return_value = {"foo": 42}
        mock_requests.return_value.status_code = 200
        ct = client.Client("foo", "http://foo_ep")

        result = ct.get("/bar", body={}, data={})
        mock_requests.assert_called_with("GET", "http://foo_ep/bar",
                                         body={}, data={})
        self.assertEqual(({"foo": 42}, 200), result)

        result = ct.put("/bar", body={}, data={})
        mock_requests.assert_called_with("PUT", "http://foo_ep/bar",
                                         body={}, data={})
        self.assertEqual(({"foo": 42}, 200), result)

        result = ct.post("/bar", body={}, data={})
        mock_requests.assert_called_with("POST", "http://foo_ep/bar",
                                         body={}, data={})
        self.assertEqual(({"foo": 42}, 200), result)

        result = ct.delete("/bar", body={}, data={})
        mock_requests.assert_called_with("DELETE", "http://foo_ep/bar",
                                         body={}, data={})
        self.assertEqual(({"foo": 42}, 200), result)
