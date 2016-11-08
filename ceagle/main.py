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
import logging
import os

import flask
from flask_helpers import routing  # noqa

from ceagle.api.v1 import capacity
from ceagle.api.v1 import cloud_status
from ceagle.api.v1 import infrastructure
from ceagle.api.v1 import intelligence
from ceagle.api.v1 import optimization
from ceagle.api.v1 import security


app = flask.Flask(__name__)
config_path = os.environ.get("CEAGLE_CONF", "etc/ceagle/config.json")

try:
    config = json.load(open(config_path))
    app.config.update(config)
except IOError as e:
    logging.warning("Config at '%s': %s" % (config_path, e))


@app.errorhandler(404)
def not_found(error):
    return flask.jsonify({"error": "Not Found"}), 404


for bp in [cloud_status, infrastructure, intelligence, optimization, security,
           capacity]:
    for url_prefix, blueprint in bp.get_blueprints():
        app.register_blueprint(blueprint, url_prefix="/api/v1%s" % url_prefix)


app = routing.add_routing_map(app, html_uri=None, json_uri="/api/v1")


def main():
    app.run(host=app.config.get("HOST", "0.0.0.0"),
            port=app.config.get("PORT", 5000))


if __name__ == "__main__":
    main()
