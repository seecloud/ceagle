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

import requests

from ceagle.api import base
from ceagle.api_fake_data import fake_security
from ceagle import config

FAKE_CLIENT_MAP = {
    "security": fake_security.Client,
}


class UnknownService(Exception):
    pass


class Client(base.Client):

    def get(self, uri="/", **kwargs):
        """Make GET request and decode JSON data.

        :param uri: resource URI
        :param kwargs: query parameters
        :returns: dict response data
        """
        url = "%s%s" % (self.endpoint, uri)
        try:
            response = requests.get(url, **kwargs)
        except requests.exceptions.ConnectionError:
            mesg = "Service '%(name)s' is not available at '%(endpoint)s'" % (
                {"name": self.name, "endpoint": self.endpoint})
            return {"error": {"message": mesg}}, 502
        try:
            result = response.json()
        except ValueError:
            return {"error": {"message": "Response can not be decoded"}}, 500

        return result, response.status_code


def get_client(service_name):
    """Return client for given service name, if possible.

    :param service_name: str name of microservice
    :returns: Client
    """
    if config.get_config().get("use_fake_api_data", True):
        client_class = FAKE_CLIENT_MAP.get(service_name)
        if client_class is None:
            raise NotImplementedError(
                "Fake client for '%s' is not implemented" % service_name)
    else:
        client_class = Client
    endpoint = config.get_config().get("services", {}).get(service_name)
    if endpoint:
        return client_class(name=service_name, endpoint=endpoint)
    raise UnknownService("Unknown service '%s'" % service_name)
