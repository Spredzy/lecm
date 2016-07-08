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


def main():

    options = parser.parse()

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
        for name, parameters in certificates.iteritems():
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
                        cert.reload_service()
            elif options.renew:
                if options.noop:
                    if cert.days_before_expiry <= cert.remaining_days:
                        noop_holder[name] = parameters
                else:
                    if cert.days_before_expiry <= cert.remaining_days:
                        cert.renew()
                        cert.reload_service()
        if options.noop:
            lists.list(noop_holder)
