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

import argparse

from oss_lib import config

from ceagle import app
from ceagle import config as cfg


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host",
                        default="0.0.0.0",
                        help="A host to bind development server. "
                             "(default 0.0.0.0)")
    parser.add_argument("--port",
                        type=int,
                        default=5000,
                        help="A port to bind development server. "
                             "(default 5000)")
    args = config.process_args("CEAGLE",
                               parser=parser,
                               default_config_path=cfg.DEFAULT_CONF_PATH,
                               defaults=cfg.DEFAULT,
                               validation_schema=cfg.SCHEMA)
    app.app.config["DEBUG"] = args.debug
    app.app.run(host=args.host, port=args.port)
