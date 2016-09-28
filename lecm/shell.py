# Copyright 2016 Yanis Guenane <yguenane@redhat.com>
# Author: Yanis Guenane <yguenane@redhat.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from lecm import certificate
from lecm import configuration
from lecm import lists
from lecm import parser
from lecm import utils

import logging
import os


def should_reload(cert, global_configuration):

    if cert.service_name != global_configuration.get('service_name', 'httpd'):
        return True

    return False


def main():

    options = parser.parse()

    if options.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    _CHANGE = False
    _CONF = {}
    if options.conf:
        _CONF['file_path'] = options.conf

    global_configuration = configuration.load_configuration(_CONF)
    certificates = configuration.expand_configuration(global_configuration)
    certificates = utils.filter_certificates(options.items, certificates)

    if options.list:
        lists.list(certificates)
    elif options.list_details:
        lists.list_details(certificates)
    else:
        noop_holder = {}
        for name, parameters in certificates.items():
            cert = certificate.Certificate(parameters)
            if options.generate:
                if options.noop:
                    if not os.path.exists('%s/pem/%s.pem' %
                                          (cert.path, cert.name)):
                        noop_holder[name] = parameters
                else:
                    if not os.path.exists('%s/pem/%s.pem' %
                                          (cert.path, cert.name)):
                        cert.generate()
                        _CHANGE = True
                        # If the service for a specific certificate is
                        # different than the 'default' service_name or
                        # no default is specified then reload the service
                        # right after certificate generation, else reload
                        # it just once at the end
                        if should_reload(cert, global_configuration):
                            cert.reload_service()
            elif options.renew:
                if options.noop:
                    if cert.days_before_expiry <= cert.remaining_days:
                        noop_holder[name] = parameters
                else:
                    if cert.days_before_expiry <= cert.remaining_days:
                        cert.renew()
                        _CHANGE = True
                        # If the service for a specific certificate is
                        # different than the 'default' service_name or
                        # no default is specified then reload the service
                        # right after certificate generation, else reload
                        # it just once at the end
                        if should_reload(cert, global_configuration):
                            cert.reload_service()

        if not options.noop and _CHANGE:
            utils.reload_service(
                global_configuration.get('service_name', 'httpd'),
                global_configuration.get('service_provider', 'systemd')
            )
        if options.noop:
            lists.list(noop_holder)


if __name__ == "__main__":
    main()
