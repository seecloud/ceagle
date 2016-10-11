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

import json
import os

import flask

from ceagle.blueprints.cloud_status import cloud_status


app = flask.Flask(__name__)

app.config.from_object(__name__)
app.config.update({"SECRET_KEY": "change_this_key_in_prod"})
app.config.from_envvar("CEAGLE_SETTINGS", silent=True)


@app.route("/", methods=["GET"])
def index():
    return flask.render_template("index.html", menu="index", title="Index")


@app.route("/about", methods=["GET"])
def about():
    return flask.render_template("about.html",
                                 menu="about", title="About")


@app.errorhandler(404)
def not_found(error):
    return flask.render_template("errors/not_found.html",
                                 menu="error",
                                 title="Not Found"), 404


for url_prefix, blueprint in cloud_status.get_blueprints():
    app.register_blueprint(blueprint, url_prefix=url_prefix)


@app.context_processor
def inject_config():
    load_config()
    return dict(cloud_status_conf=app.config["cloud_status"],
                global_conf=app.config["global"])


CONFIG_LOADED = False


def load_config(path=None):
    global CONFIG_LOADED

    if CONFIG_LOADED:
        return

    CONFIG_LOADED = True
    path = path or os.environ.get("CEAGLE_CONF", "/etc/ceagle/config.json")

    try:
        with open(path) as f:
            config = json.load(f)
    except IOError as e:
        print("Config at '%s': %s" % (path, e))
        config = {}

    app.config.update(config.get("flask", {}))
    app.config["cloud_status"] = config.get("cloud_status",
                                            {"enabled": False})
    app.config["global"] = config.get("global", {"portal_name": "Cloud Eagle"})


def main():
    load_config()
    app.run(host=app.config.get("HOST", "0.0.0.0"),
            port=app.config.get("PORT", 5000))


if __name__ == "__main__":
    main()
