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


RESPONSE_TOTAL_NULL_PROBABILITY = 10
HEALTH_NULL_PROBABILITY = 5
PERFORMANCE_NULL_PROBABILITY = 5
AVAILABILITY_NULL_PROBABILITY = 5
STATUS_NULL_PROBABILITY = 20


def validate_period(period):
    if period not in ("day", "week", "month", "year"):
        flask.abort(404)


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


def lucky(probability):
    """Return a boolean status with given probability.

    :param probability: int <= 100,
                        0 will always cause False result
    :rtype: bool
    """
    if probability:
        return random.randint(1, 100) <= probability
    return False


def generate_values(period_or_timestamps,
                    ratio=1, null_probability=20, integer=False):
    if type(period_or_timestamps) == list:
        timestamps = period_or_timestamps
    else:
        timestamps = generate_timestamps(period_or_timestamps)
    if timestamps:
        data = []
        data_avg = []
        for ts in timestamps:
            if lucky(null_probability):
                data.append([ts, None])
            else:
                if not integer:
                    value = base.randnum(.7, 1) * ratio
                else:
                    value = random.randint(1, 1000)
                data.append([ts, value])
                data_avg.append(value)
        avg = round(sum(data_avg) / len(data_avg), 3)
        return (data, avg)


def generate_service_data(period, service, null_allowed):
    if service == "health":
        null_probability = null_allowed and HEALTH_NULL_PROBABILITY or 0

        fci_data = generate_values(period, 1, null_probability)[0]
        time_data = generate_values(period, 1, null_probability)[0]
        size_data = generate_values(
            period, 50, null_probability, integer=True)[0]
        count_data = generate_values(
            period, 50, null_probability, integer=True)[0]
        return {
            "fci": random.randint(0, 100) * 0.01,
            "response_time": base.randnum(.1, 2.5),
            "response_size": random.randint(2000, 5000),
            "api_calls_count": random.randint(200, 500),
            "fci_data": fci_data,
            "response_time_data": time_data,
            "response_size_data": size_data,
            "api_calls_count_data": count_data
        }

    elif service == "performance":
        null_probability = null_allowed and PERFORMANCE_NULL_PROBABILITY or 0
        data, avg = generate_values(period, 1, null_probability)
        return {"data": data, "duration": avg}

    elif service == "availability":
        null_probability = null_allowed and AVAILABILITY_NULL_PROBABILITY or 0
        data, avg = generate_values(period, 1, null_probability)
        return {"availability_data": data, "availability": avg}


def generate_region_data(region, period, service, null_allowed):
    data = fake_regions.regions(detailed=True).get(region)

    if not data:
        return ({"error": "Region '%s' not found" % region}, 404)

    if service not in data["services"]:
        error = ("Service '%s' is not available for region '%s'"
                 % (service, region))
        return ({"error": error}, 404)

    result = generate_service_data(period, service, null_allowed)
    return ({service: {region: result}, "period": period}, 200)


def generate_status_data(period, service):
    null_allowed = lucky(RESPONSE_TOTAL_NULL_PROBABILITY)
    data = {}
    for region in fake_regions.regions():
        result, code = generate_region_data(region, period, service,
                                            null_allowed)
        if code == 200:
            data.update(result[service])
    return flask.jsonify({"period": period, service: data})


@base.api_handler
def get_status(period):
    validate_period(period)
    status = {}
    rand = lambda: None if lucky(STATUS_NULL_PROBABILITY) else random.random()
    for region in fake_regions.regions():
        status[region] = {"sla": rand(),
                          "performance": random.randint(1, 10),
                          "availability": rand(),
                          "health": rand()}
    return flask.jsonify({"status": status, "period": period})


@base.api_handler
def get_status_health(period):
    validate_period(period)
    return generate_status_data(period, "health")


@base.api_handler
def get_status_performance(period):
    validate_period(period)
    return generate_status_data(period, "performance")


@base.api_handler
def get_status_availability(period):
    validate_period(period)
    return generate_status_data(period, "availability")


@base.api_handler
def get_region_status(region, period):
    validate_period(period)
    data = fake_regions.regions(detailed=True).get(region)
    if not data:
        return ({"error": "Region '%s' not found" % region}, 404)

    if lucky(RESPONSE_TOTAL_NULL_PROBABILITY):
        rand = lambda: (None if lucky(STATUS_NULL_PROBABILITY)
                        else random.random())
    else:
        rand = random.random

    status = {}
    for service in ("keystone", "nova", "cinder"):
        status[service] = {"sla": rand(),
                           "performance": random.randint(1, 10),
                           "availability": rand(),
                           "health": rand()}
    return flask.jsonify({"status": status, "period": period})


@base.api_handler
def get_region_status_health(region, period):
    validate_period(period)
    null_allowed = lucky(RESPONSE_TOTAL_NULL_PROBABILITY)
    result, code = generate_region_data(
        region, period, "health", null_allowed)
    return flask.jsonify(result), code


@base.api_handler
def get_region_status_performance(region, period):
    validate_period(period)
    null_allowed = lucky(RESPONSE_TOTAL_NULL_PROBABILITY)
    result, code = generate_region_data(
        region, period, "performance", null_allowed)
    return flask.jsonify(result), code


@base.api_handler
def get_region_status_availability(region, period):
    validate_period(period)
    region_data = fake_regions.regions(detailed=True).get(region)

    if not region_data:
        return flask.jsonify({"error": "Region '%s' not found" % region}), 404

    if "availability" not in region_data["services"]:
            error = ("Service '%s' is not available for region '%s'"
                     % ("availability", region))
            return flask.jsonify({"error": error}), 404

    null_probability = (lucky(RESPONSE_TOTAL_NULL_PROBABILITY)
                        and PERFORMANCE_NULL_PROBABILITY or 0)

    availability = {}
    for svc in ["foo_service", "bar_service", "spam_service"]:
        data, avg = generate_values(period, 1, null_probability)
        availability[svc] = {"availability_data": data,
                             "availability": avg}

    return flask.jsonify({"availability": availability,
                          "region": region,
                          "period": period})
