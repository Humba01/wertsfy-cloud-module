#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from tempest import config
from tempest import test

CONF = config.CONF


class BaseSenlinTest(test.BaseTestCase):

    credentials = ['primary', 'admin']

    default_params = config.service_client_config()

    # NOTE: Tempest uses timeout values of compute API if project specific
    # timeout values don't exist.
    default_params_with_timeout_values = {
        'build_interval': CONF.compute.build_interval,
        'build_timeout': CONF.compute.build_timeout
    }
    default_params_with_timeout_values.update(default_params)

    client = None

    max_api_version = '1.0'

    @classmethod
    def skip_checks(cls):
        super(BaseSenlinTest, cls).skip_checks()
        if not CONF.service_available.senlin:
            skip_msg = 'Senlin is disabled'
            raise cls.skipException(skip_msg)

    @classmethod
    def setup_clients(cls):
        super(BaseSenlinTest, cls).setup_clients()

    @classmethod
    def resource_setup(cls):
        super(BaseSenlinTest, cls).resource_setup()
        cls.max_api_version = cls.client.get_max_api_version()
