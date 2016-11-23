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


REGIONS_NUM = 4


def regions(detailed=False):
    """Generate fake regions."""
    tpl = itertools.cycle(["west-%i.hooli.net", "north-%i.piedpiper.net",
                           "east-%i.hooli.net", "south-%i.piedpiper.net"])
    idx = itertools.count(1)
    srv = itertools.cycle([
        ["health", "performance", "cis"],
        ["health", "availability", "performance", "cis", "security"],
        ["health", "security"]])

    result = {} if detailed else []

    for i in range(REGIONS_NUM):
        region = next(tpl) % next(idx)
        if detailed:
            result[region] = {"services": next(srv)}
        else:
            result.append(region)
    return result


@base.api_handler
def get_regions(detailed):
    return flask.jsonify({"regions": regions(detailed=detailed)})
