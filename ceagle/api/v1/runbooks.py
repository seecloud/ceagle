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
from ceagle.api_fake_data import fake_runbooks


bp = flask.Blueprint("runbooks", __name__)


@bp.route("/runbooks", methods=["GET"])
@bp.route("/region/<region>/runbooks",
          methods=["GET", "POST"])
@fake_runbooks.handle_runbooks
def handle_runbooks(region=''):
    api_endpoint = "/api/v1/region/{}/runbooks".format(region)

    if flask.request.method == "GET":
        read_client = client.get_client("runbook-read")
        if not region:
            api_endpoint = "/api/v1/runbooks"
        params = flask.request.args
        result, code = read_client.get(api_endpoint, params=params)
    else:  # POST
        write_client = client.get_client("runbook-write")
        new_runbook = flask.request.get_json(silent=True) or {}
        result, code = write_client.post(api_endpoint, json=new_runbook)
    return flask.jsonify(result), code


@bp.route("/region/<region>/runbooks/<book_id>",
          methods=["GET", "PUT", "DELETE"])
@fake_runbooks.handle_single_runbook
def handle_single_runbook(region, book_id):
    api_endpoint = "/api/v1/region/{}/runbooks/{}".format(
        region, book_id)

    if flask.request.method == "GET":
        read_client = client.get_client("runbook-read")
        result, code = read_client.get(api_endpoint)
    elif flask.request.method == "PUT":
        write_client = client.get_client("runbook-write")
        new_runbook = flask.request.get_json(silent=True) or {}
        result, code = write_client.put(api_endpoint, json=new_runbook)
    elif flask.request.method == "DELETE":
        write_client = client.get_client("runbook-write")
        result, code = write_client.delete(api_endpoint)
    return flask.jsonify(result), code


@bp.route("/region/<region>/runbooks/<book_id>/run",
          methods=["POST"])
@fake_runbooks.run_runbook
def run_runbook(region, book_id):
    run_client = client.get_client("runbook-run")
    run_settings = flask.request.get_json(silent=True) or {}
    api_endpoint = "/api/v1/region/{}/runbooks/{}/run".format(region, book_id)
    result, code = run_client.post(api_endpoint, json=run_settings)
    return flask.jsonify(result), code


@bp.route("/runbook_runs")
@bp.route("/region/<region>/runbook_runs")
@fake_runbooks.runbook_runs
def runbook_runs(region=None):
    read_client = client.get_client("runbook-read")
    if region:
        api_endpoint = "/api/v1/region/{}/runbook_runs".format(region)
    else:
        api_endpoint = "/api/v1/runbook_runs"
    params = flask.request.args
    result, code = read_client.get(api_endpoint, params=params)
    return flask.jsonify(result), code


@bp.route("/region/<region>/runbook_runs/<run_id>")
@fake_runbooks.single_runbook_run
def single_runbook_run(region, run_id):
    read_client = client.get_client("runbook-read")
    api_endpoint = "/api/v1/region/{}/runbook_runs/{}".format(region, run_id)
    params = flask.request.args
    result, code = read_client.get(api_endpoint, params=params)
    return flask.jsonify(result), code


def get_blueprints():
    return [
        ["", bp],
    ]
