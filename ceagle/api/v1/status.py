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

from ceagle.api import client
from ceagle.api_fake_data import fake_status


bp_status = flask.Blueprint("status", __name__)
bp_region_status = flask.Blueprint("region", __name__)


@bp_status.route("/<period>")
@fake_status.get_status
def get_status(period):
    return flask.jsonify("fixme!")


@bp_status.route("/health/<period>")
@fake_status.get_status_health
def get_status_health(period):
    health_client = client.get_client("health")
    if not health_client:
        return (flask.jsonify({"error": "No health endpoint configured"}),
                404)

    api_endpoint = "/api/v1/health/{}".format(period)

    result, code = health_client.get(api_endpoint)
    return flask.jsonify(result), code


@bp_status.route("/performance/<period>")
@fake_status.get_status_performance
def get_status_performance(period):
    return flask.jsonify("fixme!")


@bp_status.route("/availability/<period>")
@fake_status.get_status_availability
def get_status_availability(period):
    ct = client.get_client("availability")
    if not ct:
        err = {"error": "No availability endpoint configured"}
        return flask.jsonify(err), 404

    api_endpoint = "/api/v1/availability/{period}".format(period=period)
    resp, code = ct.get(api_endpoint)
    return flask.jsonify(resp), code


@bp_region_status.route("/<region>/status/<period>")
@fake_status.get_region_status
def get_region_status(region, period):
    return flask.jsonify("fixme!")


@bp_region_status.route("/<region>/status/health/<period>")
@fake_status.get_region_status_health
def get_region_status_health(region, period):
    health_client = client.get_client("health")
    if not health_client:
        return (flask.jsonify({"error": "No health endpoint configured"}),
                404)

    api_endpoint = "/api/v1/region/{region}/health/{period}".format(
        region=region, period=period)

    result, code = health_client.get(api_endpoint)
    return (flask.jsonify(result),
            code)


@bp_region_status.route("/<region>/status/performance/<period>")
@fake_status.get_region_status_performance
def get_region_status_performance(region, period):
    return flask.jsonify("fixme!")


@bp_region_status.route("/<region>/status/availability/<period>")
@fake_status.get_region_status_availability
def get_region_status_availability(region, period):
    ct = client.get_client("availability")
    if not ct:
        err = {"error": "No availability endpoint configured"}
        return flask.jsonify(err), 404
    api_endpoint = "/api/v1/region/{region}/availability/{period}".format(
        region=region, period=period)
    resp, code = ct.get(api_endpoint)
    return flask.jsonify(resp), code


def get_blueprints():
    return [
        ["/status", bp_status],
        ["/region", bp_region_status]
    ]
