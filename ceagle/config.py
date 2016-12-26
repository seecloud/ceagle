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

DEFAULT_CONF_PATH = "/etc/ceagle/config.json"

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
                "properties": {
                    "pages": {
                        "type": "array",
                        "uniqueItems": True,
                        "items": {
                            "type": "object",
                            "properties": {
                                "title": {
                                    "type": "string",
                                    "minLength": 1,
                                },
                                "full_title": {
                                    "type": "string",
                                    "minLength": 1,
                                },
                                "menu": {
                                    "type": "string",
                                    "minLength": 1,
                                },
                                "description": {
                                    "type": "string",
                                    "minLength": 1,
                                },
                                "iframe": {
                                    "type": "string",
                                    "minLength": 1,
                                },
                            },
                            "required": ["title", "full_title", "menu",
                                         "description", "iframe"],
                            "additionalProperties": False,
                        },
                    },
                },
                "required": ["pages"],
                "additionalProperties": False,
            },
        },
        "additionalProperties": False,
    },
}
