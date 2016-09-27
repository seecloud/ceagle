#
#
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

import random

import flask


def gen_values(mode):

    if mode == 1:
        gen = lambda: random.uniform(0.9, 1)
    elif mode == 2:
        gen = lambda: random.randint(20, 2000)
    elif mode == 3:
        gen = lambda: random.randint(100, 40000)

    return [["24-Sep-16T%s" % i, gen()] for i in range(24)]

app = flask.Flask(__name__)

app.config.from_object(__name__)
app.config.update({"SECRET_KEY": "change_this_key_in_prod"})
app.config.from_envvar("CLOUDEAGLE_SETTINGS", silent=True)
app.config.from_pyfile('/etc/cloud-eagle/config.cfg', silent=True)


@app.route("/", methods=["GET"])
def index():
    return flask.render_template("index.html", menu="index", title="Index")


@app.route("/health", methods=["GET"])
def health():
    return flask.render_template("health.html",
                                 menu="api_health", title="API Health")


@app.route("/health/data", methods=["GET"])
@app.route("/health/data/<for_period>", methods=["GET"])
def health_data(for_period="last_day"):

    return flask.jsonify(**{
        "project_names": ["keystone", "nova", "glance", "cinder", "neutron"],
        "projects": {

            "keystone": {
                "fci": 0.9,
                "fci_score_data": gen_values(1),
                "response_time_data": gen_values(2),
                "response_size_data": gen_values(3)
            },
            "nova": {
                "fci": 1.0,
                "fci_score_data": gen_values(1),
                "response_time_data": gen_values(2),
                "response_size_data": gen_values(3)
            },
            "glance": {
                "fci": 0.96,
                "fci_score_data": gen_values(1),
                "response_time_data": gen_values(2),
                "response_size_data": gen_values(3)
            },
            "cinder": {
                "fci": 0.995,
                "fci_score_data": gen_values(1),
                "response_time_data": gen_values(2),
                "response_size_data": gen_values(3)

            },
            "neutron": {
                "fci": 0.999,
                "fci_score_data": gen_values(1),
                "response_time_data": gen_values(2),
                "response_size_data": gen_values(3)

            }
        }
    })


@app.route("/about", methods=["GET"])
def about():
    return flask.render_template("about.html",
                                 menu="about", title="About")


@app.errorhandler(404)
def not_found(error):
    return flask.render_template("errors/not_found.html",
                                 menu="error",
                                 title="Not Found"), 404


def main():
    app.run(host=app.config.get("HOST", "0.0.0.0"),
            port=app.config.get("PORT", 5000))


if __name__ == "__main__":
    main()
