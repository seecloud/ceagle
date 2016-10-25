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

"""Base code for all services."""

import flask
from flask import views


class ServiceAPI(views.MethodView):
    """Base class for services."""

    ROUTES = None

    def __init__(self, *args, **kwargs):
        super(ServiceAPI, self).__init__(*args, **kwargs)
        self.request = flask.request

    def dispatch_request(self, *args, **kwargs):
        data = super(ServiceAPI, self).dispatch_request(*args, **kwargs)
        try:
            response = flask.jsonify(data)
        except Exception as e:
            # TODO(amaretskiy): Handle errors in proper way
            response = flask.jsonify({"error": str(e)})
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return response
