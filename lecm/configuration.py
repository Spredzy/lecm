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

from lecm import exceptions

import logging
import os
import yaml


LOG = logging.getLogger(__name__)

_FIELDS = ['type', 'size', 'digest', 'version', 'subjectAltName',
           'countryName', 'stateOrProvinceName', 'localityName',
           'organizationName', 'organizationUnitName', 'commonName',
           'emailAddress', 'account_key_name', 'path', 'remaining_days',
           'service_name', 'service_provider', 'environment']


def check_configuration_file_existence(configuration_file_path=None):
    """Check if the configuration file is present."""

    if configuration_file_path:
        if not os.path.exists(configuration_file_path):
            raise exceptions.ConfigurationExceptions(
                      'File %s does not exist' % configuration_file_path
                  )
        file_path = configuration_file_path
    elif os.getenv('LECM_CONFIGURATION'):
        if not os.path.exists(os.getenv('LECM_CONFIGURATION')):
            raise exceptions.ConfigurationExceptions(
                      'File %s does not exist' %
                      os.getenv('LECM_CONFIGURATION')
                  )
        file_path = os.getenv('LECM_CONFIGURATION')
    else:
        if not os.path.exists('/etc/lecm.conf'):
            raise exceptions.ConfigurationExceptions(
                'File /etc/lecm.conf does not exist (you could specify an '
                'alternate location using --conf)'
            )
        file_path = '/etc/lecm.conf'

    LOG.debug('Configuration file used: %s' % file_path)
    return file_path


def load_configuration(conf):
    """Load the lecm configuration file."""

    file_path = check_configuration_file_existence(conf.get('file_path'))

    try:
        file_path_content = open(file_path, 'r').read()
    except IOError as exc:
        raise exceptions.ConfigurationExceptions(exc)

    try:
        conf = yaml.load(file_path_content)
    except yaml.YAMLError as exc:
        raise exceptions.ConfigurationExceptions(exc)

    return conf


def expand_configuration(configuration):
    """Fill up certificates with defaults."""

    certificates = {}
    for name, parameters in configuration['certificates'].items():
        if not isinstance(parameters, dict):
            parameters = {}
        parameters['name'] = name
        for field in _FIELDS:
            if field not in parameters.keys() or parameters[field] is None:
                if field in configuration:
                    parameters[field] = configuration[field]
        certificates[name] = parameters

    return certificates
