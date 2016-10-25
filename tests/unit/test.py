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
import testtools

from ceagle import main


class TestCase(testtools.TestCase):

    def setUp(self):
        super(TestCase, self).setUp()
        main.app.config["TESTING"] = True
        self.app = main.app.test_client()

    def test_load_config(self):
        pass

    @mock.patch("ceagle.main.flask.render_template", return_value="foo_api")
    def test_index(self, mock_render_template):
        main.api_map = "api map"
        rv = self.app.get("/")
        self.assertEqual(200, rv.status_code)
        self.assertIn("foo_api", str(rv.data))
        mock_render_template.assert_called_once_with(
            "api_index.html", api="api map")

    @mock.patch("ceagle.main.flask.jsonify", return_value="foo_json")
    def test_not_found(self, mock_jsonify):
        rv = self.app.get("/unexisting/path/to/somewhere/else")
        self.assertEqual(404, rv.status_code)
        self.assertIn("foo_json", str(rv.data))
        mock_jsonify.assert_called_once_with({"error": "Not found"})
