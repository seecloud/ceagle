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

import datetime
import random

import flask
from werkzeug import exceptions

from ceagle.api_fake_data import base
from ceagle.api_fake_data import fake_regions


def generate_values(days, ratio=1):
    today = datetime.date.today()
    if days == 1:
        ystday = (today - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        stamps = ["%sT%.2i:00" % (ystday, hr) for hr in range(24)]
    else:
        stamps = [(today - datetime.timedelta(days=(days - d)))
                  for d in range(days)]
        stamps = [s.strftime("%Y-%m-%dT00:00") for s in stamps]
    data = [[s, base.randnum(.7, 1) * ratio] for s in stamps]
    avg = round(sum([v[1] for v in data]) / len(data), 3)
    return (data, avg)


def generate_service_data(days, service):
    if service == "health":
        fci_data = generate_values(days)[0]
        time_data = generate_values(days)[0]
        size_data = generate_values(days, 50)[0]
        return {
            "fci": random.randint(2000, 5000),
            "response_time": base.randnum(.1, 2.5),
            "response_size": random.randint(2000, 5000),
            "api_calls_count": random.randint(200, 500),
            "fci_data": fci_data,
            "response_time_data": time_data,
            "repsonse_size_data": size_data
        }

    elif service == "performance":
        data, avg = generate_values(days)
        return {"data": data, "duration": avg}

    elif service == "availability":
        data, avg = generate_values(days)
        return {"data": data, "availability": avg}


def generate_region_data(region, period, service=None):
    data = fake_regions.regions(detailed=True).get(region)
    days = base.PERIODS.get(period)

    if not days:
        raise exceptions.NotFound

    if not data:
        return ({"error": "Region '%s' not found" % region}, 404)

    if service:
        if service not in data["services"]:
            error = ("Service '%s' is not available for region '%s'"
                     % (service, region))
            return ({"error": error}, 404)

        result = generate_service_data(days, service)
        return ({service: {region: result}, "period": period}, 200)

    result = {"sla": base.randnum(.7, 1)}
    for service in ("availability", "performance", "health"):
        if service in data["services"]:
            result[service] = generate_service_data(days, service)

    return ({"period": period, "status": {region: result}}, 200)


def generate_status_data(period, service=None):
    data = {}
    for region in fake_regions.regions():
        result, code = generate_region_data(region, period, service)
        if code == 200:
            if service:
                data.update(result[service])
            else:
                data.update(result["status"])
    service = service or "status"
    return flask.jsonify({"period": period, service: data})


def generate_region_data_response(region, period, service=None):
    result, code = generate_region_data(region, period, service)
    return (flask.jsonify(result), code)


@base.api_handler
def get_status(period):
    return generate_status_data(period)


@base.api_handler
def get_status_health(period):
    return generate_status_data(period, "health")


@base.api_handler
def get_status_performance(period):
    return generate_status_data(period, "performance")


@base.api_handler
def get_status_availability(period):
    return generate_status_data(period, "availability")


@base.api_handler
def get_region_status(region, period):
    return generate_region_data_response(region, period)


@base.api_handler
def get_region_status_health(region, period):
    return generate_region_data_response(region, period, "health")


@base.api_handler
def get_region_status_performance(region, period):
    return generate_region_data_response(region, period, "performance")


@base.api_handler
def get_region_status_availability(region, period):
    return generate_region_data_response(region, period, "availability")
