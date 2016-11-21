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

from ceagle.api_fake_data import base
from ceagle.api_fake_data import fake_regions


def generate_infra_services():
    return [
        {
            "menu": "Jenkins",
            "title": "Jenkins CI/CD system",
            "description": "Some description about this service",
            "url": "https://1.2.3.4:12345"
        },
        {
            "menu": "Stacklight",
            "title": "Logging, Metering and Alerting systems",
            "description": "Some description about this service",
            "url": "https://1.2.3.4:12345"
        }]


@base.api_handler
def get_region_infra(region):
    data = fake_regions.regions(True).get(region)

    if not data:
        return flask.jsonify({"error": "Region '%s' not found" % region}), 404

    services = generate_infra_services()
    return flask.jsonify({"region": region, "services": services})
