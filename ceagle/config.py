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
import logging
import os


config = None


def get_config():
    """Return cached configuration.

    :returns: application config
    :rtype: dict
    """
    global config
    if not config:
        path = os.environ.get("CEAGLE_CONF", "/etc/ceagle/config.json")
        try:
            config = json.load(open(path))
            logging.info("Config is '%s'" % path)
        except IOError as e:
            logging.warning("Config at '%s': %s" % (path, e))
            config = {
                "flask": {
                    "HOST": "0.0.0.0",
                    "PORT": 5000,
                    "DEBUG": False
                }
            }
    return config
