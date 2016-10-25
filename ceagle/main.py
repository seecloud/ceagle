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

from __future__ import print_function
import os

import flask

from ceagle.services import v1


app = flask.Flask(__name__)
api_map = []


def load_config():
    conf_defaults = {"SECRET_KEY": "change_this_key_in_prod"}
    app.config.update(conf_defaults)

    settings = os.environ.get("CEAGLE_CONF", "settings_local")
    try:
        app.config.from_object(settings)
    except ImportError:
        print("Module '%s' is not found. Using defaults..." % settings)


def register_routes(svc_classes, uri_prefix=""):
    for cls in svc_classes:
        for i, route in enumerate(cls.ROUTES):
            route_uri, options = route
            uri = uri_prefix + route_uri
            endpoint = ".".join((cls.__module__, cls.__name__))
            api_map.append({"uri": uri,
                            "methods": cls.methods,
                            "endpoint": endpoint,
                            "doc": cls.__doc__})
            view = cls.as_view(endpoint + "#%i" % i)
            print("Registering route: %s -> %s" % (uri, endpoint))
            app.add_url_rule(uri, view_func=view, **options)

load_config()
register_routes(v1.SERVICES, "/api/v1")


@app.route("/")
def index():
    """Expose APIs for development porposes."""
    return flask.render_template("api_index.html", api=api_map)


@app.errorhandler(404)
def not_found(error):
    return flask.jsonify({"error": "Not found"}), 404


def main():
    app.run(host=app.config.get("HOST", "0.0.0.0"),
            port=app.config.get("PORT", 5000))


if __name__ == "__main__":
    main()
