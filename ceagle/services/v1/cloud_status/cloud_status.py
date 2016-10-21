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

from ceagle.api_fake_data import cloud_status_data
from ceagle.services import service


class Overview(service.ServiceAPI):
    """Cloud status overview."""

    ROUTES = [("/cloud_status/", {})]

    def get(self):
        return cloud_status_data.overview_data()


class Health(service.ServiceAPI):
    """Cloud health."""

    ROUTES = [("/cloud_status/health/", {"defaults": {"region": "all"}}),
              ("/cloud_status/health/<region>", {})]

    def get(self, region):
        period = self.request.args.get("period", "day")
        if period == "day":
            period = "now-1d/m"
            interval = "10m"
        elif period == "week":
            period = "now-7d/m"
            interval = "1h"
        else:
            period = "now-30d/m"
            interval = "4h"

        interval

        # TODO(amaretskiy): get data by region and period

        return cloud_status_data.health_projects()


class Availability(service.ServiceAPI):
    """Cloud availability."""

    ROUTES = [("/cloud_status/availability/", {"defaults": {"region": "all"}}),
              ("/cloud_status/availability/<region>", {})]

    def get(self, region):
        return cloud_status_data.availability_data()
