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
import sys


def should_reload(cert, global_configuration):

    if cert.service_name != global_configuration.get('service_name', 'httpd'):
        return True

    return False


def main():

    options = parser.parse()

    if isinstance(options, int):
        sys.stderr.write(
            'USAGE: lecm [--generate,--renew,--list,--list-details]\n'
        )
        return 1

    if options.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

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
        certs = []
        certs_w_service_name = []
        services_to_restart = []

        for name, parameters in certificates.items():
            cert = certificate.Certificate(parameters)
            if options.generate:
                if options.noop:
                    if not os.path.exists('%s/pem/%s.pem' %
                                          (cert.path, cert.name)):
                        noop_holder[name] = parameters
                else:
                    if not os.path.exists('%s/pem/%s.pem' %
                                          (cert.path, cert.name)) or \
                       options.force:
                        cert.generate()
                        certs.append(cert)
                        if 'service_name' in parameters:
                            certs_w_service_name.append(cert)
                            if not isinstance(parameters['service_name'], list):  # noqa
                                services_to_restart.append(
                                    [parameters['service_name']]
                                )
                            else:
                                services_to_restart.append(
                                    parameters['service_name']
                                )

            elif options.renew:
                if options.noop:
                    if isinstance(cert.days_before_expiry, int) and \
                       cert.days_before_expiry <= cert.remaining_days:
                        noop_holder[name] = parameters
                else:
                    if (isinstance(cert.days_before_expiry, int) and
                       cert.days_before_expiry <= cert.remaining_days) or \
                       options.force:
                        cert.renew()
                        certs.append(cert)
                        if 'service_name' in parameters:
                            certs_w_service_name.append(cert)
                            if not isinstance(parameters['service_name'], list):  # noqa
                                services_to_restart.append(
                                    [parameters['service_name']]
                                )
                            else:
                                services_to_restart.append(
                                    parameters['service_name']
                                )

        if len(certs) != len(certs_w_service_name):
            services_to_restart.append(
                global_configuration.get('service_name', ['httpd'])
            )

        if certs and not options.noop:
            utils.reload_service(
                list(set(sum(services_to_restart, []))),
                global_configuration.get('service_provider', 'systemd')
            )
        if options.noop:
            lists.list(noop_holder)


if __name__ == "__main__":
    main()
