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
from lecm import utils

import os


def list(certificates):
    result = [['Item', []],
              ['Status', []],
              ['subjectAltName', []],
              ['Location', []],
              ['Days', []]]
    for name, parameters in certificates.items():
        cert = certificate.Certificate(parameters)

        result[0][1].append(cert.name)
        if os.path.exists('%s/pem/%s.pem' % (cert.path, cert.name)):
            result[1][1].append('Generated')
        else:
            result[1][1].append('Not-Generated')
        result[2][1].append(cert.subjectAltName)
        result[3][1].append('%s/pem/%s.pem' % (cert.path, cert.name))
        result[4][1].append(cert.days_before_expiry)

    utils.output_informations(result)


def list_details(certificates):
    result = [['Item', []],
              ['Status', []],
              ['subjectAltName', []],
              ['emailAddress', []],
              ['Location', []],
              ['Type', []],
              ['Size', []],
              ['Digest', []],
              ['Days', []]]
    for name, parameters in certificates.items():
        cert = certificate.Certificate(parameters)

        result[0][1].append(cert.name)
        if os.path.exists('%s/pem/%s.pem' % (cert.path, cert.name)):
            result[1][1].append('Generated')
        else:
            result[1][1].append('Not-Generated')
        result[2][1].append(cert.subjectAltName)
        result[3][1].append(cert.subject['emailAddress'])
        result[4][1].append('%s/pem/%s.pem' % (cert.path, cert.name))
        result[5][1].append(cert.type)
        result[6][1].append(cert.size)
        result[7][1].append(cert.digest)
        result[8][1].append(cert.days_before_expiry)

    utils.output_informations(result)
