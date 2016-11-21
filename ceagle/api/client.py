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

from ceagle import config


class Client(object):
    """REST client."""

    def __init__(self, name, conf, **kwargs):
        self.name = name
        self.config = conf
        self.endpoint = conf["endpoint"]

    def __repr__(self):
        return "<Client '%s'>" % self.name

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
            return {"status_code": 502,
                    "error": {"message": mesg}}
        try:
            result = response.json()
        except ValueError:
            return {"status_code": 500,
                    "error": {"message": "Response can not be decoded"}}
        result.setdefault("status_code", response.status_code)
        return result


def get_client(service_name):
    """Return client for given service anme, if possible.

    :param service_name: str name of microservice
    :returns: Client
    """
    conf = config.get_config().get(service_name)
    if (conf and conf.get("endpoint")):
        return Client(name=service_name, conf=conf)
    return None
