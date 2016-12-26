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

from oss_lib import config

from ceagle import app
from ceagle import config as cfg


def main():
    config.process_args("CEAGLE",
                        default_config_path=cfg.DEFAULT_CONF_PATH,
                        defaults=cfg.DEFAULT,
                        validation_schema=cfg.SCHEMA)
    app_conf = config.CONF["flask"]
    app.app.config.update(app_conf)
    app.app.run(host=app_conf["HOST"], port=app_conf["PORT"])
