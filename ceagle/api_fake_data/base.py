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

import functools
import random

from ceagle import config


USE_FAKE_DATA = config.get_config().get("use_fake_api_data", True)


def api_handler(fake):
    """Function that handles api_fake_data substitution functions

    It is intended to be used as a decorator around fake api functions. It
    turns a function it decorates into a decorator, that accepts "real" api
    function (real_function_handler). The resulting decorator returns a
    (choice_maker) function, that calls real or fake function, depending on the
    value of USE_FAKE_DATA global variable.
    """
    def real_function_handler(real):
        @functools.wraps(real)
        def choice_maker(*args, **kwargs):
            if USE_FAKE_DATA:
                return fake(*args, **kwargs)
            return real(*args, **kwargs)
        return choice_maker
    return real_function_handler


def randnum(from_num, to_num, round_by=2):
    return round(from_num + ((to_num - from_num) * random.random()), round_by)
