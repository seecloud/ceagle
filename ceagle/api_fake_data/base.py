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

import functools
import random
import re

from ceagle import config

USE_FAKE_DATA = config.get_config().get("use_fake_api_data", True)


def route(reg):
    def decorator(method):
        method._route = re.compile("^%s$" % reg)
        return method
    return decorator


class FakeClient(object):
    """Base fake client.

    Usage:

    >>> from ceagle.api_fake_data import base
    >>> class MyClient(base.FakeClient):
    ...  @base.route(r"/api/(?P<method>)")
    ...  def _method(self, query, method):
    ...   return {"query": query}, 200
    ...
    >>> c = MyClient(name="name", endpoint="endpoint")
    >>> resp, code = c.get("/api/foo", foo="bar")
    >>> assert code == 200
    >>> assert resp == {"query": {"foo": "bar"}}

    """

    def __init__(self, name, endpoint):
        self._setup_routing()

    def _setup_routing(self):
        self._routes = []
        for attr in dir(self):
            method = getattr(self, attr)
            route = getattr(method, "_route", None)
            if route:
                self._routes.append((route, method))

    def _find_route(self, path):
        for reg, method in self._routes:
            match = reg.match(path)
            if match:
                return method, match
        return None, None

    def default(self, path, *args, **kwargs):
        return ("not found", 404)

    def get(self, path, **kwargs):
        method, match = self._find_route(path)
        if method is None:
            return self.default(path, **kwargs)
        return method(kwargs, **match.groupdict())


def api_handler(fake):
    """Function that handles api_fake_data substitution functions

    It is intended to be used as a decorator around fake api functions. It
    turns a function it decorates into a decorator, that accepts "real" api
    function (real_function_handler). The resulting decorator returns a
    (choice_maker) function, that calls real or fake function, depending on the
    value of USE_FAKE_DATA global variable.
    """
    def real_function_handler(real):
        @functools.wraps(real)
        def choice_maker(*args, **kwargs):
            if USE_FAKE_DATA:
                return fake(*args, **kwargs)
            return real(*args, **kwargs)
        return choice_maker
    return real_function_handler


def randnum(from_num, to_num, round_by=2):
    return round(from_num + ((to_num - from_num) * random.random()), round_by)
