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

from ceagle.api import base


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
    "Region1": [
        _get_fake_issue("Region1", "IssueType1", 2),
        _get_fake_issue("Region1", "IssueType2", 8),
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


class Client(base.Client):

    def get(self, uri="/", **kwargs):
        """Make GET request and decode JSON data.

        :param uri: resource URI
        :param kwargs: query parameters
        :returns: dict response data
        """
        region, security, issues, period = uri.split("/")
        if issues != "issues":
            return {"error": "Not found"}, 404
        issues = []
        all_issues = FAKE_ISSUES.get(region)
        if all_issues:
            now = datetime.datetime.now()
            try:
                discovered_before = (now - datetime.timedelta(
                    days=PERIOD_MAP[period])).isoformat("T")
            except KeyError:
                return {"error": "Not found"}, 404
            for issue in all_issues:
                if issue["discovered_at"] >= discovered_before:
                    issues.append(issue)
        else:
            return {"error": "Region not found"}, 404
        return {"issues": issues}, 200
