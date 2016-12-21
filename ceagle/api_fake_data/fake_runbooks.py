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

import datetime
import random

import flask

from ceagle.api_fake_data import base


def get_single_runbook():
    tag_choices = [
        ["Monitoring"],
        ["Databases"],
        ["Monitoring", "Databases"],
        None
    ]
    tags = random.choice(tag_choices)
    runbook = {
        "_id": str(random.randint(1, 1000)),
        "description": "Demo runbook description",
        "name": "Demo runbook",
        "type": "bash",
        "runbook": "IyEvYmluL2Jhc2gKCmVjaG8gIkhlbGxvIFdvcmxkISIK"
    }
    if tags:
        runbook["tags"] = tags
    return runbook


def get_single_run():
    finished_at = datetime.datetime.now().isoformat()
    started_at = (datetime.datetime.now() - datetime.timedelta(
        minutes=random.randint(1, 20))).isoformat()
    return {
        "_id": str(random.randint(1, 1000)),
        "started_at": started_at,
        "finished_at": finished_at,
        "user": "cloud_user",
        "output": "SGVsbG8gV29ybGQhCg==",
        "return_code": 0,
    }


@base.api_handler
def handle_runbooks(region):
    if flask.request.method == "POST":
        body = flask.request.get_json(silent=True) or {}
        for field in ["description", "name",
                      "runbook", "type"]:
            if field not in body:
                return flask.jsonify(
                    {"error": "missing {}".format(field)}), 400
        body["_id"] = str(random.randint(1, 1000))
        return flask.jsonify(body), 201
    return flask.jsonify(
        {"runbooks": [get_single_runbook() for i in range(10)]}
    )


@base.api_handler
def handle_single_runbook(region, book_id):
    if flask.request.method == "GET":
        return flask.jsonify(get_single_runbook())
    elif flask.request.method == "PUT":
        body = flask.request.get_json(silent=True) or {}
        for field in ["description", "name",
                      "runbook", "type"]:
            if field not in body:
                return flask.jsonify(
                    {"error": "missing {}".format(field)}), 400
        body["_id"] = book_id
        return flask.jsonify(body)
    elif flask.request.method == "DELETE":
        return '', 204


@base.api_handler
def run_runbook(region, book_id):
    run = get_single_run()
    run['finished_at'] = None
    run['output'] = None
    run['return_code'] = None
    return flask.jsonify(run), 202


@base.api_handler
def runbook_runs(region):
    return flask.jsonify(
        {"runs": [get_single_run() for i in range(10)]}
    )


@base.api_handler
def single_runbook_run(region, run_id):
    return flask.jsonify(get_single_run()), 200
