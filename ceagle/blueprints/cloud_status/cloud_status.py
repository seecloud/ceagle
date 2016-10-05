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


overview = flask.Blueprint("overview", __name__,
                           template_folder="templates")

health = flask.Blueprint("health", __name__,
                         template_folder="templates")

availability = flask.Blueprint("availability", __name__,
                               template_folder="templates")


def get_blueprints():
    return [
        ["/cloud_status/", overview],
        ["/cloud_status/health", health],
        ["/cloud_status/availability", availability]
    ]


@overview.route("/")
def overview_index():
    return flask.render_template("overview.html",
                                 menu="cloud_status",
                                 submenu="overview",
                                 title="Cloud Status Overview")


@overview.route("/v1", defaults={"region": "all"})
@overview.route("/v1/<region>")
def overview_data_v1(region):
    return flask.jsonify(**{})


@health.route("/")
def health_index():
    return flask.render_template("health.html",
                                 menu="cloud_status",
                                 submenu="health",
                                 title="Cloud Status Health")


@health.route("/v1", defaults={"region": "all"})
@health.route("/v1/<region>")
def health_data_v1(region):
    return cloud_status_data.health_projects()


@availability.route("/")
def availability_index():
    return flask.render_template("availability.html",
                                 menu="cloud_status",
                                 submenu="availability",
                                 title="API Health")


@availability.route("/v1", defaults={"region": "all"})
@availability.route("/v1/<region>")
def availability_data_v1(region):
    return flask.jsonify(**{})
