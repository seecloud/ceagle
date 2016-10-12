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

import flask
import requests

from ceagle.api_fake_data import cloud_status_data


overview = flask.Blueprint("overview", __name__,
                           template_folder="templates")

health = flask.Blueprint("health", __name__,
                         template_folder="templates")

availability = flask.Blueprint("availability", __name__,
                               template_folder="templates")


def get_blueprints():
    return [
        ["/cloud_status", overview],
        ["/cloud_status/health", health],
        ["/cloud_status/availability", availability]
    ]


@overview.route("/")
def overview_index():
    return flask.render_template("overview.html",
                                 menu="cloud_status",
                                 submenu="overview",
                                 title="Cloud Status Overview")


@overview.route("/v1")
@overview.route("/v1/")
def overview_data_v1():
    return cloud_status_data.overview_data()


@health.route("/", defaults={"region": "all"})
@health.route("/<region>")
def health_index(region):
    return flask.render_template("health.html",
                                 menu="cloud_status",
                                 submenu="health",
                                 title="Cloud Status Health")


@health.route("/v1", defaults={"region": "all"})
@health.route("/v1/<region>")
def health_data_v1(region):
    return cloud_status_data.health_projects()

    period = flask.request.args.get("period", "day")

    if period == "day":
        period = "now-1d/m"
        interval = "10m"
    elif period == "week":
        period = "now-7d/m"
        interval = "1h"
    else:
        period = "now-30d/m"
        interval = "4h"

    query = {
        "query": {
            "filtered": {
                "filter": {
                    "range": {
                        "timestamp": {
                            "gte": period
                        }
                    }
                }
            }
        },
        "aggs": {
            "projects": {
                "terms": {"field": "service"},

                "aggs": {
                    "avg_fci": {
                        "avg": {
                            "field": "fci"
                        }
                    },
                    "data": {
                        "date_histogram": {
                            "field": "timestamp",
                            "interval": interval,
                            "format": "yyyy-MM-dd'T'hh:mm",
                            "min_doc_count": 0
                        },
                        "aggs": {
                            "fci": {
                                "avg": {"field": "fci"}
                            },
                            "response_size": {
                                "avg": {"field": "response_time.avg"}
                            },
                            "response_time": {
                                "avg": {"field": "response_size.avg"}
                            }
                        }
                    }
                }
            }
        }
    }

    # TODO(boris-42): support regions
    request = flask.current_app.config[
        "cloud_status"]["regions"][0]["health"]["elastic"]
    r = requests.get("%s/_search?search_type=count" % request,
                     data=json.dumps(query))

    result = {
        "project_names": [],
        "projects": {}
    }

    def convert_(data, field):
        result = []
        for d in data["buckets"]:
            result.append([d["key_as_string"], d[field]["value"]])
        return result

    for project in r.json()["aggregations"]["projects"]["buckets"]:
        result["project_names"].append(project["key"])
        result["projects"][project["key"]] = {
            "fci": project["avg_fci"]["value"],
            "fci_score_data": convert_(project["data"], "fci"),
            "response_time_data": convert_(project["data"], "response_time"),
            "response_size_data": convert_(project["data"], "response_size")
        }

    return flask.jsonify(**result)


@availability.route("/", defaults={"region": "all"})
@availability.route("/<region>")
def availability_index(region):
    return flask.render_template("availability.html",
                                 menu="cloud_status",
                                 submenu="availability",
                                 title="API Health")


@availability.route("/v1", defaults={"region": "all"})
@availability.route("/v1/<region>")
def availability_data_v1(region):
    return cloud_status_data.availability_data()
