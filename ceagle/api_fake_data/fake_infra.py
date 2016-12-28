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

import itertools

import flask

from ceagle.api_fake_data import base
from ceagle.api_fake_data import fake_regions


INFRAS = [
    [{"id": "horizon",
      "title": "Horizon",
      "description": "Web UI that manages OpenStack resources",
      "urls": [["http://none"]]},
     {"id": "git",
      "title": "Git Source Control",
      "description": ("Gitlab with Git repositories with all "
                      "projects source code"),
      "urls": [["http://none"]]},
     {"id": "packages",
      "title": "JFrog Artifactory Packages",
      "description": ("JFrog Artifactory service that contains "
                      "all cloud packages & images"),
      "urls": [["http://none"]]},
     {"id": "stacklight",
      "title": "Stacklight",
      "description": "Cloud Logging, Metering and Alerting services",
      "urls": [["http://none"]]}],
    [{"id": "horizon",
      "title": "Horizon",
      "description": "Web UI that manages OpenStack resources",
      "urls": [["http://none"]]},
     {"id": "baremetal",
      "title": "Baremetal Provisioning",
      "description": "MaaS service that manages baremetal infrastructure",
      "urls": [["http://none"]]},
     {"id": "jenkins",
      "title": "Jenkins CI/CD",
      "description": "Cloud Continues Integration and Deployment.",
      "urls": [["http://none"]]}]]


@base.api_handler
def get_region_infra(region):
    regions = fake_regions.regions()
    if region not in regions:
        return flask.jsonify({"error": "Region '%s' not found" % region}), 404
    infra_idx = regions.index(region) % len(INFRAS)
    return flask.jsonify({"region": region, "infra": INFRAS[infra_idx]})


@base.api_handler
def get_regions_infra():
    infras = itertools.cycle(INFRAS)
    infra = {region: next(infras) for region in fake_regions.regions()}
    return flask.jsonify({"infra": infra})
