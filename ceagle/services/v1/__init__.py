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

from ceagle.services.v1.capacity import capacity
from ceagle.services.v1.cloud_status import cloud_status
from ceagle.services.v1.infrastructure import infrastructure
from ceagle.services.v1.intelligence import intelligence
from ceagle.services.v1.optimization import optimization
from ceagle.services.v1.security import security


SERVICES = (capacity.Overview,
            cloud_status.Overview,
            cloud_status.Health,
            cloud_status.Availability,
            infrastructure.Overview,
            infrastructure.RemotePage,
            intelligence.Overview,
            optimization.Overview,
            security.Overview)
