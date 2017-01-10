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

from oss_lib import config
import requests

from ceagle.api import base
from ceagle.api_fake_data import security

CONF = config.CONF

FAKE_CLIENT_MAP = {
    "security": security.Client,
}


class UnknownService(Exception):
    pass


class Client(base.Client):

    def request(self, method="GET", uri="/", **kwargs):
        """Make `method` request and decode JSON data.

        :param uri: resource URI
        :param kwargs: query parameters
        :returns: tuple: response data-dict and response code
        """
        url = "%s%s" % (self.endpoint, uri)
        try:
            response = requests.request(method, url, **kwargs)
        except requests.exceptions.ConnectionError:
            mesg = "Service '%(name)s' is not available at '%(endpoint)s'" % (
                {"name": self.name, "endpoint": self.endpoint})
            return {"error": {"message": mesg}}, 502

        # NO_CONTENT means we have nothing to decode
        # expected for DELETE methods for example
        if response.status_code == 204:
            return "", response.status_code

        try:
            result = response.json()
        except ValueError:
            return {"error": {
                "message": "Response can not be decoded"}}, 500

        return result, response.status_code

    def get(self, uri="/", **kwargs):
        """Make GET request and decode JSON data.

        :param uri: resource URI
        :param kwargs: query parameters
        :returns: tuple: response data-dict and response code
        """
        return self.request("GET", uri, **kwargs)

    def post(self, uri="/", **kwargs):
        """Make POST request and decode JSON data.

        :param uri: resource URI
        :param kwargs: query parameters
        :returns: tuple: response data-dict and response code
        """
        return self.request("POST", uri, **kwargs)

    def put(self, uri="/", **kwargs):
        """Make PUT request and decode JSON data.

        :param uri: resource URI
        :param kwargs: query parameters
        :returns: tuple: response data-dict and response code
        """
        return self.request("PUT", uri, **kwargs)

    def delete(self, uri="/", **kwargs):
        """Make DELETE request and decode JSON data.

        :param uri: resource URI
        :param kwargs: query parameters
        :returns: tuple: response data-dict and response code
        """
        return self.request("DELETE", uri, **kwargs)


def get_client(service_name):
    """Return client for given service name, if possible.

    :param service_name: str name of microservice
    :returns: Client
    """
    if CONF["use_fake_api_data"]:
        client_class = FAKE_CLIENT_MAP.get(service_name)
        if client_class is None:
            raise NotImplementedError(
                "Fake client for '%s' is not implemented" % service_name)
        return client_class(name=service_name, endpoint="_fake_")
    endpoint = CONF["services"].get(service_name)
    if endpoint:
        return Client(name=service_name, endpoint=endpoint)
    raise UnknownService("Unknown service '%s'" % service_name)
