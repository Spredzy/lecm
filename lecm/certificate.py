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

from lecm import utils
from OpenSSL import crypto

import datetime
import logging
import os
import requests
import socket
import subprocess

LOG = logging.getLogger(__name__)

_INTERMEDIATE_CERTIFICATE_URL = \
    'https://letsencrypt.org/certs/lets-encrypt-r3-cross-signed.pem'

_STAGING_URL = \
    'https://acme-staging.api.letsencrypt.org'


class Certificate(object):

    def __init__(self, conf):
        self.name = conf.get('name')
        self.path = conf.get('path')
        self.type = conf.get('type', 'RSA')
        self.size = conf.get('size', 4096)
        self.digest = conf.get('digest', 'sha256')
        self.version = conf.get('version', 3)
        self.environment = conf.get('environment', 'production')
        self.subjectAltName = self.normalize_san(conf.get('subjectAltName'))
        self.account_key_name = conf.get('account_key_name',
                                         'account_%s.key' % socket.getfqdn())
        self.remaining_days = conf.get('remaining_days', 10)
        self.days_before_expiry = self.get_days_before_expiry()
        self.service_name = conf.get('service_name', 'httpd')
        self.service_provider = conf.get('service_provider', 'systemd')

        self.subject = {
          'C': conf.get('countryName'),
          'ST': conf.get('stateOrProvinceName'),
          'L': conf.get('localityName'),
          'O': conf.get('organizationName'),
          'OU': conf.get('organizationalUnitName'),
          'CN': conf.get('commonName'),
          'emailAddress': conf.get('emailAddress'),
        }

        if self.subject['CN'] is None:
            self.subject['CN'] = self.name

        if self.subjectAltName is None:
            self.subjectAltName = 'DNS:%s' % self.name

    def normalize_san(self, san):

        # If an array of SAN is passed in the configuration file
        #
        # certificates:
        #   my.example.org:
        #     subjectAltName:
        #       - my.example.org
        #       - my1.example.org
        #
        # return : DNS:my.example.org,DNS:my1.example.org
        if isinstance(san, list):
            san_string = 'DNS:%s' % ',DNS:'.join(san)

        # If a string of SAN is passed but without the proper format
        #
        # certificates:
        #   my.example.org:
        #     subjectAltName: my.example.org,my1.example.org
        #
        # return : DNS:my.example.org,DNS:my1.example.org
        elif san and not san.startswith('DNS:'):
            san_string = 'DNS:%s' % ',DNS:'.join(san.split(','))
        else:
            san_string = 'DNS:%s' % self.name

        return san_string

    def _create_filesystem(self):
        _FOLDERS = ['csr', 'challenges', 'pem', 'private', 'certs']

        for folder in _FOLDERS:
            LOG.debug('[global] Ensure path exist: %s/%s' %
                      (self.path, folder))
            if not os.path.exists('%s/%s' % (self.path, folder)):
                os.makedirs('%s/%s' % (self.path, folder))
                utils.enforce_selinux_context(self.path)

    def _get_intermediate_certificate(self):
        certificate_name = os.path.basename(_INTERMEDIATE_CERTIFICATE_URL)
        if not os.path.exists('%s/pem/%s' % (self.path, certificate_name)):
            certificate = requests.get(_INTERMEDIATE_CERTIFICATE_URL).text

            LOG.info('[global] Getting intermediate certificate PEM file: %s' %
                     certificate_name)
            if not os.path.exists('%s/pem/%s' % (self.path, certificate_name)):
                with open('%s/pem/%s' % (self.path, certificate_name), 'w') as f:
                    f.write(certificate)

    def _create_account_key(self):
        account_key = crypto.PKey()

        if self.type == 'RSA':
            crypto_type = crypto.TYPE_RSA
        else:
            crypto_type = crypto.TYPE_DSA

        try:
            LOG.info('[global] Generating account key: %s \
                     (type: %s, size: %s)' %
                     (self.account_key_name, self.type, self.size))
            account_key.generate_key(crypto_type, self.size)
        except (TypeError, ValueError):
            raise

        try:
            LOG.debug('[global] Writting account key: %s/private/%s' %
                      (self.path, self.account_key_name))
            accountkey_file = os.open('%s/private/%s' %
                                      (self.path, self.account_key_name),
                                      os.O_WRONLY | os.O_CREAT | os.O_TRUNC,
                                      0o600)
            os.write(accountkey_file,
                     crypto.dump_privatekey(crypto.FILETYPE_PEM, account_key))
            os.close(accountkey_file)
        except IOError:
            try:
                os.remove('%s/private/%s.key' %
                          (self.path, self.account_key_name))
            except OSError:
                pass
            raise

    def _create_private_key(self):
        private_key = crypto.PKey()

        if self.type == 'RSA':
            crypto_type = crypto.TYPE_RSA
        else:
            crypto_type = crypto.TYPE_DSA

        try:
            LOG.info('[%s] Generating private key (type: %s, size: %s)' %
                     (self.name, self.type, self.size))
            private_key.generate_key(crypto_type, self.size)
        except (TypeError, ValueError):
            raise

        try:
            LOG.debug('[%s] Writting private key: %s/private/%s.key' %
                      (self.name, self.path, self.name))
            privatekey_file = os.open('%s/private/%s.key' %
                                      (self.path, self.name),
                                      os.O_WRONLY | os.O_CREAT | os.O_TRUNC,
                                      0o600)
            os.write(privatekey_file,
                     crypto.dump_privatekey(crypto.FILETYPE_PEM, private_key))
            os.close(privatekey_file)
        except IOError:
            try:
                os.remove('%s/private/%s.key' % (self.path, self.name))
            except OSError:
                pass
            raise

    def _create_csr(self):
        LOG.info('[%s] Generating CSR' % self.name)
        req = crypto.X509Req()
        LOG.debug('[%s] Attaching Certificate Version to CSR: %s' %
                  (self.name, self.version))
        req.set_version(self.version)
        subject = req.get_subject()

        for (key, value) in self.subject.items():
            if value is not None:
                LOG.debug('[%s] Attaching %s to CSR: %s' %
                          (self.name, key, value))
                setattr(subject, key, value)

        LOG.info('[%s] Attaching SAN extention: %s' %
                 (self.name, self.subjectAltName))

        try:
            req.add_extensions([crypto.X509Extension(
                bytes('subjectAltName', 'utf-8'), False,
                bytes(self.subjectAltName, 'utf-8')
            )])
        except TypeError:
            req.add_extensions([crypto.X509Extension('subjectAltName', False,
                                                     self.subjectAltName)])

        LOG.debug('[%s] Loading private key: %s/private/%s.key' %
                  (self.name, self.path, self.name))
        privatekey_content = open('%s/private/%s.key' %
                                  (self.path, self.name)).read()

        privatekey = crypto.load_privatekey(crypto.FILETYPE_PEM,
                                            privatekey_content)

        LOG.info('[%s] Signing CSR' % self.name)
        req.set_pubkey(privatekey)
        req.sign(privatekey, self.digest)

        LOG.debug('[%s] Writting CSR: %s/csr/%s.csr' %
                  (self.name, self.path, self.name))
        csr_file = open('%s/csr/%s.csr' % (self.path, self.name), 'w')
        csr_file.write((crypto.dump_certificate_request(crypto.FILETYPE_PEM,
                                                        req)).decode('utf-8'))
        csr_file.close()

    def _create_certificate(self):
        LOG.info('[%s] Retrieving certificate from Let''s Encrypt Server' %
                 self.name)
        command = 'acme-tiny --account-key %s/private/%s --csr %s/csr/%s.csr \
                  --acme-dir %s/challenges/%s' % (self.path,
                                                  self.account_key_name,
                                                  self.path, self.name,
                                                  self.path, self.name)

        if self.environment == 'staging':
            LOG.info('[%s] Using Let''s Encrypt staging API: %s' %
                     (self.name, _STAGING_URL))
            command = '%s --ca %s' % (command, _STAGING_URL)

        cert_file_f = open('%s/certs/%s.crt.new' % (self.path, self.name), 'w')

        p = subprocess.Popen(command.split(), stdout=cert_file_f,
                             stderr=subprocess.PIPE)
        out, err = p.communicate()

        if p.returncode != 0:
            LOG.error('[%s] %s' % (self.name, err))
            os.remove('%s/certs/%s.crt.new' % (self.path, self.name))
            return False
        else:
            LOG.debug('[%s] Writting certificate: %s/certs/%s.crt' %
                      (self.name, self.path, self.name))
            os.rename('%s/certs/%s.crt.new' % (self.path, self.name),
                      '%s/certs/%s.crt' % (self.path, self.name))

            LOG.debug('[%s] Concatenating certificate with intermediate pem: \
                      %s/pem/%s.pem' % (self.name, self.path, self.name))
            self._get_intermediate_certificate()
            pem_filename = os.path.basename(_INTERMEDIATE_CERTIFICATE_URL)
            filenames = ['%s/certs/%s.crt' % (self.path, self.name),
                         '%s/pem/%s' % (self.path, pem_filename)]
            with open('%s/pem/%s.pem' % (self.path, self.name), 'w') as f:
                for fname in filenames:
                    with open(fname) as infile:
                        f.write(infile.read())
        return True

    def get_days_before_expiry(self):
        try:
            x509_content = open('%s/pem/%s.pem' %
                                (self.path, self.name)).read()
        except IOError:
            return 'N/A'
        x509 = crypto.load_certificate(crypto.FILETYPE_PEM, x509_content)

        notAfter = x509.get_notAfter()[:-1]
        notAfter_datetime = datetime.datetime.strptime(
            notAfter.decode('utf-8'),
            '%Y%m%d%H%M%S'
        )
        now_datetime = datetime.datetime.now()

        return (notAfter_datetime - now_datetime).days

    def generate(self):

        self._create_filesystem()

        # Ensure there is no left-over from previous setup
        #
        try:
            LOG.info('[%s] Removing older files (if any)' % self.name)
            os.remove('%s/private/%s.key' % (self.path, self.name))
            os.remove('%s/csr/%s.csr' % (self.path, self.name))
            os.rmdir('%s/challenges/%s' % (self.path, self.name))
            os.remove('%s/certs/%s.key' % (self.path, self.name))
        except OSError:
            pass

        if not os.path.exists('%s/private/%s' %
                              (self.path, self.account_key_name)):
            self._create_account_key()
        self._create_private_key()
        self._create_csr()
        os.makedirs('%s/challenges/%s' % (self.path, self.name))
        self._create_certificate()

    def renew(self):
        self._create_csr()
        self._create_certificate()

    def reload_service(self):
        utils.reload_service(self.service_name, self.service_provider)
