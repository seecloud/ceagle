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

from ceagle.api_fake_data import fake_regions


bp = flask.Blueprint("regions", __name__)


@bp.route("/", defaults={"detailed": False})
@bp.route("/detailed", defaults={"detailed": True})
@fake_regions.get_regions
def get_regions(detailed):
    return flask.jsonify({"fixme"})


def get_blueprints():
    return [["/regions", bp]]
