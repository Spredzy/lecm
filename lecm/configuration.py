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

from swiftbackmeup import exceptions

import os
import yaml


_FIELDS = ['type', 'size', 'digest', 'version', 'subjectAltName',
           'countryName', 'stateOrProvinceName', 'localityName',
           'organizationName', 'organizationUnitName', 'commonName',
           'emailAddress', 'account_key_name', 'path', 'remaining_days']


def load_configuration():
    """Load the swiftbackmeup configuration file."""

    file_path = '../sample/lecm.conf'

    # file_path = check_configuration_file_existence(conf.get('file_path'))

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
    for name, parameters in configuration['certificates'].iteritems():
        if not isinstance(parameters, dict):
            parameters = {}
        parameters['name'] = name
        for field in _FIELDS:
            if field not in parameters.keys() or parameters[field] is None:
                if field in configuration:
                    parameters[field] = configuration[field]
        certificates[name] = parameters

    return certificates
