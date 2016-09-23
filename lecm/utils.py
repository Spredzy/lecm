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

from prettytable import PrettyTable

import copy
import logging
import os
import platform
import subprocess

LOG = logging.getLogger(__name__)


def output_informations(data):

    x = PrettyTable()
    for column in data:
        x.add_column(column[0], column[1])
    print(x)


def filter_certificates(items, certificates):

    certificates_to_return = copy.deepcopy(certificates)
    if isinstance(items, list):
        for name in certificates.keys():
            if name not in items:
                del certificates_to_return[name]

    return certificates_to_return


def enforce_selinux_context(output_directory):

    if platform.dist()[0] in ['fedora', 'centos', 'redhat']:
        if os.path.exists('/sbin/semanage'):
            FNULL = open(os.devnull, 'w')

            # Set new selinux so it is persistent over reboot
            command = 'semanage fcontext -a -t cert_t %s(/.*?)' % (
                output_directory
            )
            p = subprocess.Popen(command.split(), stdout=FNULL,
                                 stderr=subprocess.STDOUT)
            p.wait()

            # Ensure file have the right context applied
            command = 'restorecon -Rv %s' % output_directory
            p = subprocess.Popen(command.split(), stdout=FNULL,
                                 stderr=subprocess.STDOUT)
            p.wait()


def reload_service(service_name, service_provider):

    if service_name:
        LOG.info('Reloading service specified: %s' % service_name)
        if service_provider == 'sysv':
            command = 'service %s reload' % service_name
        else:
            command = 'systemctl reload %s' % service_name
        p = subprocess.Popen(command.split())
        p.wait()
