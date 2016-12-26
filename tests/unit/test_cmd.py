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

import mock

from ceagle import cmd
from tests.unit import test


class CmdTestCase(test.TestCase):
    @mock.patch("oss_lib.config.process_args")
    @mock.patch("ceagle.cmd.app.app")
    def test_main(self, mock_app, mock_process):
        self.mock_config({
            "flask": {
                "HOST": "10.0.0.2",
                "PORT": 80,
            },
        })
        cmd.main()
        mock_app.run.assert_called_once_with(host="10.0.0.2", port=80)
