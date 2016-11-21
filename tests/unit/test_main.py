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

from ceagle import main
from tests.unit import test


class AppTestCase(test.TestCase):

    def test_versions(self):
        code, resp = self.get("/api/")
        self.assertEqual(200, code)
        self.assertEqual({"versions": ["1.0"]}, resp)

    def test_not_found(self):
        code, resp = self.get("/unexisting/path/to/somewhere/else")
        self.assertEqual(404, code)
        self.assertEqual({"error": "Not Found"}, resp)

    def test_api_map(self):
        code, resp = self.get("/")
        self.assertEqual(200, code)
        part = {"endpoint": "capacity.index",
                "methods": ["GET", "HEAD", "OPTIONS"],
                "uri": "/api/v1/capacity/"}
        self.assertIn(part, resp)

    @mock.patch("ceagle.main.app")
    def test_main(self, mock_app):
        self.assertFalse(mock_app.run.called)
        main.main()
        mock_app.run.assert_called_once_with()
