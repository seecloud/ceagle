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

from ceagle.services.v1.capacity import capacity
from ceagle.services.v1.cloud_status import cloud_status
from ceagle.services.v1.infrastructure import infrastructure
from ceagle.services.v1.intelligence import intelligence
from ceagle.services.v1.optimization import optimization
from ceagle.services.v1.security import security


app = flask.Flask(__name__)

app.config.from_object(__name__)
app.config.update({"SECRET_KEY": "change_this_key_in_prod"})
app.config.from_envvar("CEAGLE_SETTINGS", silent=True)


@app.errorhandler(404)
def not_found(error):
    return flask.jsonify({"error": "Not found"}), 404


for bp in [cloud_status, infrastructure, intelligence, optimization, security,
           capacity]:
    for url_prefix, blueprint in bp.get_blueprints():
        app.register_blueprint(blueprint, url_prefix=url_prefix)


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


def main():
    load_config()
    app.run(host=app.config.get("HOST", "0.0.0.0"),
            port=app.config.get("PORT", 5000))


if __name__ == "__main__":
    main()
