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

import flask

from ceagle.api_fake_data import base


def _get_fake_issue(region, issue_type, days):
    now = datetime.datetime.now()
    discovered = now - datetime.timedelta(days=days)
    confirmed = now
    return {
        "type": issue_type,
        "description": "Sample issue " + issue_type,
        "discovered_at": discovered.isoformat(),
        "confirmed_at": confirmed.isoformat(),
        "object_id": "test-id-%s-%d" % (issue_type, days),
        "region": region,
    }

FAKE_ISSUES = {
    "region1": [
        _get_fake_issue("region1", "IssueType1", 2),
        _get_fake_issue("region1", "IssueType2", 8),
    ],
    "north-2.piedpiper.net": [
        _get_fake_issue("north-2.piedpiper.net", "IssueType1", 0),
        _get_fake_issue("north-2.piedpiper.net", "IssueType2", 2),
        _get_fake_issue("north-2.piedpiper.net", "IssueType2", 8),
    ],
}

PERIOD_MAP = {
    "day": 1,
    "week": 7,
    "month": 30,
}

REGION_R = r"(?P<region>[a-z\d\-\.\_]+)"
PERIOD_R = r"(?P<period>day|week|month)"


def _get_issues(region, period):
    issues = []
    if region:
        all_issues = FAKE_ISSUES.get(region)
        if all_issues is None:
            flask.abort(404)
    else:
        all_issues = sum(FAKE_ISSUES.values(), [])
    now = datetime.datetime.now()
    try:
        discovered_before = (now - datetime.timedelta(
            days=PERIOD_MAP[period])).isoformat("T")
    except KeyError:
        flask.abort(404)
    for issue in all_issues:
        if issue["discovered_at"] >= discovered_before:
            issues.append(issue)
    return issues


class Client(base.FakeClient):

    @base.route("/api/(?P<api>\w+)/regions")
    def _regions(self, query, api):
        return list(FAKE_ISSUES.keys()), 200

    @base.route(r"/api/v1/region/%s/security/issues/%s" % (REGION_R, PERIOD_R))
    def issues(self, query, region, period):
        return {"issues": _get_issues(region, period)}, 200

    @base.route(r"/api/v1/security/issues/%s" % PERIOD_R)
    def issues_all_regions(self, query, period):
        return {"issues": _get_issues(None, period)}, 200
