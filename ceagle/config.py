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

DEFAULT_CONF_PATH = "/etc/ceagle/config.yaml"

DEFAULT = {
    "use_fake_api_data": False,
    "services": {},
}

SCHEMA = {
    "use_fake_api_data": {"type": "boolean"},
    "services": {
        "type": "object",
        "properties": {
            "availability": {"type": "string"},
            "capacity": {"type": "string"},
            "cis": {"type": "string"},
            "health": {"type": "string"},
            "optimization": {"type": "string"},
            "performance": {"type": "string"},
            "security": {"type": "string"},
            "infra": {
                "type": "object",
                "patternProperties": {
                    "\w+": {
                        "type": "array",
                        "uniqueItems": True,
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {
                                    "type": "string",
                                    "minLength": 1,
                                },
                                "title": {
                                    "type": "string",
                                    "minLength": 1,
                                },
                                "description": {
                                    "type": "string",
                                    "minLength": 1,
                                },
                                "urls": {
                                    "type": "array",
                                    "items": {
                                        "type": "array",
                                        "items": {
                                            "type": "string",
                                            "minLength": 8
                                        }
                                    }
                                },
                            },
                            "required": ["id", "title", "description", "urls"],
                            "additionalProperties": False,
                        },
                    },
                }
            }
        },
        "additionalProperties": False,
    },
}
