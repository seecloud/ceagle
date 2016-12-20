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

from ceagle.api_fake_data import fake_runbooks


bp = flask.Blueprint("runbooks", __name__)


@bp.route("/<region>/runbooks",
          methods=["GET", "POST"])
@fake_runbooks.handle_runbooks
def handle_runbooks(region):
    return flask.jsonify("fixme!")


@bp.route("/<region>/runbooks/<book_id>",
          methods=["GET", "PUT", "DELETE"])
@fake_runbooks.handle_single_runbook
def handle_single_runbook(region, book_id):
    return flask.jsonify("fixme!")


@bp.route("/<region>/runbooks/<book_id>/run",
          methods=["POST"])
@fake_runbooks.run_runbook
def run_runbook(region, book_id):
    return flask.jsonify("fixme!")


@bp.route("/<region>/runbooks/<book_id>/runs")
@fake_runbooks.runbook_runs
def runbook_runs(region, book_id):
    return flask.jsonify("fixme!")


@bp.route("/<region>/runbooks/<book_id>/runs/<run_id>")
@fake_runbooks.single_runbook_run
def single_runbook_run(region, book_id, run_id):
    return flask.jsonify("fixme!")


def get_blueprints():
    return [
        ["/region", bp],
    ]
