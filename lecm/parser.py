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

from lecm.version import __version__

import argparse

def parse():

    parser = argparse.ArgumentParser(description='Let''s Encrypt Certificate Manager')

    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)
    parser.add_argument('--debug', action='store_true', help='Display DEBUG information level')

    parser.add_argument('--conf', help='Path to configuration file')
    parser.add_argument('-l', '--list', action='store_true',
        help='List the lecm configured certificates')
    parser.add_argument('-ld', '--list-details', action='store_true',
        help='List the lecm configured certificates (in details)')

    parser.add_argument('--generate', action='store_true',
        help='Generate Let''s Encrypt SSL Certificates')
    parser.add_argument('--renew', action='store_true',
        help='Renew already generated SSL Certificates')
    options = parser.parse_args()

    return options
