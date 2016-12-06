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

from ceagle.api_fake_data import base
from ceagle.api_fake_data import fake_regions


def period_is_valid(period):
    return period in ("day", "week", "month", "year")


def generate_timestamps(period):
    today = datetime.date.today()
    stamps = []
    if period == "day":
        day = (today - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        stamps = []
        for hour in range(24):
            for minutes in ["00", "10", "20", "30", "40", "50"]:
                stamps.append("%sT%.2i:%s" % (day, hour, minutes))
    elif period == "week":
        days = 7
        for day in [(today - datetime.timedelta(days=(days - d)))
                    for d in range(days)]:
            day = day.strftime("%Y-%m-%d")
            for hour in range(24):
                stamps.append("%sT%.2i:00" % (day, hour))
    elif period == "month":
        days = 30
        for day in [(today - datetime.timedelta(days=(days - d)))
                    for d in range(days)]:
            day = day.strftime("%Y-%m-%d")
            for hour in [0, 4, 8, 12, 16, 20]:
                stamps.append("%sT%.2i:00" % (day, hour))
    elif period == "year":
        days = 365
        for day in [(today - datetime.timedelta(days=(days - d)))
                    for d in range(days)]:
            day = day.strftime("%Y-%m-%d")
            for hour in [0, 8, 16]:
                stamps.append("%sT%.2i:00" % (day, hour))
    return stamps


def generate_values(period_or_timestamps,
                    ratio=1, null_result_probability=20):
    if type(period_or_timestamps) == list:
        timestamps = period_or_timestamps
    else:
        timestamps = generate_timestamps(period_or_timestamps)
    if timestamps:
        data = []
        data_avg = []
        for ts in timestamps:
            if random.randint(1, 100) <= null_result_probability:
                data.append([ts, None])
            else:
                value = base.randnum(.7, 1) * ratio
                data.append([ts, value])
                data_avg.append(value)
        avg = round(sum(data_avg) / len(data_avg), 3)
        return (data, avg)


def generate_service_data(period, service):
    if service == "health":
        fci_data = generate_values(period)[0]
        time_data = generate_values(period)[0]
        size_data = generate_values(period, 50)[0]
        return {
            "fci": random.randint(0, 100) * 0.01,
            "response_time": base.randnum(.1, 2.5),
            "response_size": random.randint(2000, 5000),
            "api_calls_count": random.randint(200, 500),
            "fci_data": fci_data,
            "response_time_data": time_data,
            "repsonse_size_data": size_data
        }

    elif service == "performance":
        data, avg = generate_values(period)
        return {"data": data, "duration": avg}

    elif service == "availability":
        data, avg = generate_values(period)
        return {"availability_data": data, "availability": avg}


def generate_region_data(region, period, service=None):
    data = fake_regions.regions(detailed=True).get(region)

    if not data:
        return ({"error": "Region '%s' not found" % region}, 404)

    if service:
        if service not in data["services"]:
            error = ("Service '%s' is not available for region '%s'"
                     % (service, region))
            return ({"error": error}, 404)

        result = generate_service_data(period, service)
        return ({service: {region: result}, "period": period}, 200)

    result = {"sla": base.randnum(.7, 1)}
    for service in ("availability", "performance", "health"):
        if service in data["services"]:
            result[service] = generate_service_data(period, service)

    return ({"period": period, "status": {region: result}}, 200)


def generate_status_data(period, service):
    if not period_is_valid(period):
        return flask.jsonify({"error": "Not Found"}), 404

    data = {}
    for region in fake_regions.regions():
        result, code = generate_region_data(region, period, service)
        if code == 200:
            data.update(result[service])
    return flask.jsonify({"period": period, service: data})


def generate_region_data_response(region, period, service=None):
    if not period_is_valid(period):
        return flask.jsonify({"error": "Not Found"}), 404

    result, code = generate_region_data(region, period, service)
    return (flask.jsonify(result), code)


@base.api_handler
def get_status(period):
    if not period_is_valid(period):
        flask.abort(404)
    status = {}
    rand = random.random
    for region in fake_regions.regions():
        status[region] = {
            "sla": rand() if rand() > 0.4 else None,
            "performance": random.randint(1, 10),
            "availability": rand() if rand() > 0.4 else None,
            "health": rand() if rand() > 0.4 else None
        }
    return flask.jsonify({"status": status, "period": period})


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
    if not period_is_valid(period):
        flask.abort(404)

    data = fake_regions.regions(detailed=True).get(region)
    if not data:
        return ({"error": "Region '%s' not found" % region}, 404)

    status = {}
    rand = random.random
    for service in ("keystone", "nova", "cinder"):
        status[service] = {
            "sla": rand() if rand() > 0.4 else None,
            "performance": random.randint(1, 10),
            "availability": rand() if rand() > 0.4 else None,
            "health": rand() if rand() > 0.4 else None
        }
    return flask.jsonify({"status": status, "period": period})


@base.api_handler
def get_region_status_health(region, period):
    return generate_region_data_response(region, period, "health")


@base.api_handler
def get_region_status_performance(region, period):
    return generate_region_data_response(region, period, "performance")


@base.api_handler
def get_region_status_availability(region, period):
    if not period_is_valid(period):
        return flask.jsonify({"error": "Not Found"}), 404

    region_data = fake_regions.regions(detailed=True).get(region)

    if not region_data:
        return flask.jsonify({"error": "Region '%s' not found" % region}), 404

    if "availability" not in region_data["services"]:
            error = ("Service '%s' is not available for region '%s'"
                     % ("availability", region))
            return flask.jsonify({"error": error}), 404

    availability = {}
    for svc in ["foo_service", "bar_service", "spam_service"]:
        data, avg = generate_values(period)
        availability[svc] = {"availability_data": data,
                             "availability": avg}

    return flask.jsonify({"availability": availability,
                          "region": region,
                          "period": period})
