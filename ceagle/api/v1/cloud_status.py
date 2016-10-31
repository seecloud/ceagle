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

import flask

from ceagle.api_fake_data import cloud_status_data


overview = flask.Blueprint("overview", __name__)

health = flask.Blueprint("health", __name__)

availability = flask.Blueprint("availability", __name__)


def get_blueprints():
    return [
        ["/cloud_status", overview],
        ["/cloud_status/health", health],
        ["/cloud_status/availability", availability]
    ]


@overview.route("/")
def get_status():
    return flask.jsonify(cloud_status_data.overview_data())


@health.route("/", defaults={"region": "all"})
@health.route("/<region>")
def get_health(region):
    return flask.jsonify(cloud_status_data.health_projects())


@availability.route("/", defaults={"region": "all"})
@availability.route("/<region>")
def get_availability(region):
    return flask.jsonify(cloud_status_data.availability_data())
