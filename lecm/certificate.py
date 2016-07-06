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

from OpenSSL import crypto

import datetime
import os
import requests
import subprocess

_INTERMEDIATE_CERTIFICATE_URL = 'https://letsencrypt.org/certs/lets-encrypt-x3-cross-signed.pem'

class Certificate(object):

    def __init__(self, conf):
        self.name = conf.get('name')
        self.path = conf.get('path')
        self.type = conf.get('type')
        self.size = conf.get('size', 4096)
        self.digest = conf.get('digest', 'sha256')
        self.version = conf.get('version', 3)
        self.subjectAltName = self.normalize_san(conf.get('subjectAltName'))
        self.account_key_name = conf.get('account_key_name')
        self.remaining_days = conf.get('remaining_days', 10)
        self.days_before_expiry = self.get_days_before_expiry()

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
          san_string = 'DNS;%s' % ',DNS:'.join(san)

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
            if not os.path.exists('%s/%s' % (self.path, folder)):
                os.makedirs('%s/%s' % (self.path, folder))


    def _get_intermediate_certificate(self):
        certificate = requests.get(_INTERMEDIATE_CERTIFICATE_URL).text
        certificate_name = os.path.basename(_INTERMEDIATE_CERTIFICATE_URL)

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
            account_key.generate_key(crypto_type, self.size)
        except (TypeError, ValueError):
            raise #PrivateKeyError(get_exception())

        try:
            accountkey_file = open('%s/private/%s' %
                                   (self.path, self.account_key_name), 'w')
            accountkey_file.write(crypto.dump_privatekey(crypto.FILETYPE_PEM,
                                                         account_key))
            accountkey_file.close()
        except IOError:
            try:
                os.remove('%s/private/%s.key' %
                         (self.path, self.account_key_name))
            except OSError:
                pass
            raise #PrivateKeyError(get_exception())


    def _create_private_key(self):
        private_key = crypto.PKey()

        if self.type == 'RSA':
            crypto_type = crypto.TYPE_RSA
        else:
            crypto_type = crypto.TYPE_DSA

        try:
            private_key.generate_key(crypto_type, self.size)
        except (TypeError, ValueError):
            raise #PrivateKeyError(get_exception())

        try:
            privatekey_file = open('%s/private/%s.key' %
                                   (self.path, self.name), 'w')
            privatekey_file.write(crypto.dump_privatekey(crypto.FILETYPE_PEM,
                                                         private_key))
            privatekey_file.close()
        except IOError:
            try:
                os.remove('%s/private/%s.key' % (self.path, self.name))
            except OSError:
                pass
            raise #PrivateKeyError(get_exception())


    def _create_csr(self):
        req = crypto.X509Req()
        req.set_version(self.version)
        subject = req.get_subject()

        for (key,value) in self.subject.items():
            if value is not None:
                setattr(subject, key, value)

        if self.subjectAltName is not None:
            req.add_extensions([crypto.X509Extension('subjectAltName', False,
                                                     self.subjectAltName)])

        privatekey_content = open('%s/private/%s.key' %
                                  (self.path, self.name)).read()

        privatekey = crypto.load_privatekey(crypto.FILETYPE_PEM,
                                            privatekey_content)

        req.set_pubkey(privatekey)
        req.sign(privatekey, self.digest)

        csr_file = open('%s/csr/%s.csr' % (self.path, self.name), 'w')
        csr_file.write(crypto.dump_certificate_request(crypto.FILETYPE_PEM,
                                                       req))
        csr_file.close()


    def _create_certificate(self):
       command = 'acme-tiny --account-key %s/private/%s --csr %s/csr/%s.csr --acme-dir %s/challenges/%s' % (self.path, self.account_key_name, self.path, self.name, self.path, self.name)

       cert_file_f = open('%s/certs/%s.crt' % (self.path, self.name), 'w')


       FNULL = open(os.devnull, 'w')
       p = subprocess.Popen(command.split(), stdout=cert_file_f, stderr=FNULL)
       p.wait()

       filenames = ['%s/certs/%s.crt' % (self.path, self.name),
                    '%s/pem/%s' % (self.path, os.path.basename(_INTERMEDIATE_CERTIFICATE_URL))]
       with open('%s/pem/%s.pem' % (self.path, self.name), 'w') as outfile:
           for fname in filenames:
               with open(fname) as infile:
                   outfile.write(infile.read())


    def get_days_before_expiry(self):
        try:
            x509_content = open('%s/pem/%s.pem' % (self.path, self.name)).read()
        except IOError:
            return 'N/A'
        x509 = crypto.load_certificate(crypto.FILETYPE_PEM, x509_content)

        notAfter = x509.get_notAfter()[:-1]
        notAfter_datetime = datetime.datetime.strptime(notAfter, '%Y%m%d%H%M%S')
        now_datetime = datetime.datetime.now()

        return (notAfter_datetime - now_datetime).days


    def generate_or_renew(self):

        self._create_filesystem()
        self._get_intermediate_certificate()
        if not os.path.exists('%s/private/%s' %
                              (self.path, self.account_key_name)):
            self._create_account_key()

        if not os.path.exists('%s/private/%s.key' %
                              (self.path, self.name)):
            self._create_private_key()

        if not os.path.exists('%s/csr/%s.csr' %
                              (self.path, self.name)):
            self._create_csr()

        if not os.path.exists('%s/challenges/%s' % (self.path, self.name)):
            os.makedirs('%s/challenges/%s' % (self.path, self.name))

        if not os.path.exists('%s/certs/%s.key' %
                              (self.path, self.name)):
            self._create_certificate()
