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


def _gen_values(mode):
    if mode == 1:
        return [["2016-09-16T%s:00" % i, random.uniform(0.9997, 1)]
                for i in range(24)]
    elif mode == 2:
        return [["2016-09-16T%s:00" % i, random.randint(20, 2000)]
                for i in range(24)]
    else:
        return [["2016-09-16T%s:00" % i, random.randint(100, 40000)]
                for i in range(24)]


def health_projects():
    return flask.jsonify(**{
        "project_names": ["keystone", "nova", "glance", "cinder", "neutron"],
        "projects": {

            "keystone": {
                "fci": 0.9,
                "fci_score_data": _gen_values(1),
                "response_time_data": _gen_values(2),
                "response_size_data": _gen_values(3)
            },
            "nova": {
                "fci": 1.0,
                "fci_score_data": _gen_values(1),
                "response_time_data": _gen_values(2),
                "response_size_data": _gen_values(3)
            },
            "glance": {
                "fci": 0.96,
                "fci_score_data": _gen_values(1),
                "response_time_data": _gen_values(2),
                "response_size_data": _gen_values(3)
            },
            "cinder": {
                "fci": 0.995,
                "fci_score_data": _gen_values(1),
                "response_time_data": _gen_values(2),
                "response_size_data": _gen_values(3)

            },
            "neutron": {
                "fci": 0.999,
                "fci_score_data": _gen_values(1),
                "response_time_data": _gen_values(2),
                "response_size_data": _gen_values(3)

            }
        }
    })


def overview_data():
    return flask.jsonify(**{
        "region_names": ["west-1.hooli.net",
                         "west-2.hooli.net",
                         "south-1.hooli.net"],
        "regions": {
            "west-1.hooli.net": {
                "fci": 1.0,
                "availability": 0.99999
            },
            "west-2.hooli.net": {
                "fci": 1.0,
                "availability": 0.99916
            },
            "south-1.hooli.net": {
                "fci": 0.85,
                "availability": 0.95
            }
        }
    })


def availability_data():

    data = [_gen_values(1) for i in range(3)]
    data = list(map(lambda x: [x, sum(x_[1] for x_ in x) / len(x)], data))

    return flask.jsonify(**{
        "project_names": ["nova", "glance", "cinder"],
        "projects": {
            "nova": {
                "availability": data[0][1],
                "availability_data": data[0][0]
            },
            "glance": {
                "availability": data[1][1],
                "availability_data": data[1][0]
            },
            "cinder": {
                "availability": data[2][1],
                "availability_data": data[2][0]
            },

        }
    })
