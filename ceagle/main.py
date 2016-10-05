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

from ceagle.blueprints.cloud_status import cloud_status


app = flask.Flask(__name__)

app.config.from_object(__name__)
app.config.update({"SECRET_KEY": "change_this_key_in_prod"})
app.config.from_envvar("CEAGLE_SETTINGS", silent=True)
app.config.from_pyfile('/etc/ceagle/config.cfg', silent=True)


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


def main():
    app.run(host=app.config.get("HOST", "0.0.0.0"),
            port=app.config.get("PORT", 5000))


if __name__ == "__main__":
    main()
