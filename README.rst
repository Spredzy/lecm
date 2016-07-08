========================================
lecm: Let's Encrypt Certificates Manager
========================================

|buildstatus|_ |release|_


`Let's Encrypt`_ Certificates Manager (lecm) is an
utility that allows one to manage (generate and renew) Let's Encrypt SSL
certificates.

Goal
----

The goal of ``lecm`` is to be able to generate and renew
`Let's Encrypt`_  SSL certificates automatically.

``lecm`` is configuration driven. Each certificate that needs to be managed
is described in the configuration file.


How to run it
-------------

``lecm`` is configuration driven. The configuration file is (by order of
priority):

1. The one specified on the command line (``lecm --conf /path/to/conf.yml``)
2. The one specified in the environment variable ``$LECM_CONFIGURATION``
3. The ``/etc/lecm.conf``

``lecm`` supports various commands:


``--generate``
^^^^^^^^^^^^^^

``lecm --generate`` will generate SSL certificates for items listed in the
configuration file that are not present in the filesystem.


``--renew``
^^^^^^^^^^^

``lecm --renew`` will renew SSL certificates already present on the filesystem
if its expiry date is lower than the ``remainin_days`` value.

``--list``
^^^^^^^^^^

``lecm --list`` will display basic informations about currently configured items.


.. code-block::

  +----------------------------------+---------------+------------------------------------------------------------------+-----------------------------------------------------------+------+
  |               Item               |     Status    |                          subjectAltName                          |                          Location                         | Days |
  +----------------------------------+---------------+------------------------------------------------------------------+-----------------------------------------------------------+------+
  |   lecm-test.distributed-ci.io    |   Generated   |                 DNS:lecm-test.distributed-ci.io                  |    /etc/letsencrypt/pem/lecm-test.distributed-ci.io.pem   |  89  |
  | lecm-test-test.distributed-ci.io | Not-Generated | DNS;lecm-test-test.distributed-ci.io,DNS:lecm.distributedi-ci.io | /etc/letsencrypt/pem/lecm-test-test.distributed-ci.io.pem | N/A  |
  +----------------------------------+---------------+------------------------------------------------------------------+-----------------------------------------------------------+------+


``--list-details``
^^^^^^^^^^^^^^^^

``lecm --list-details`` will display details informations about currently configured items.

.. code-block::

  +----------------------------------+---------------+------------------------------------------------------------------+---------------------------+-----------------------------------------------------------+------+------+--------+------+
  |               Item               |     Status    |                          subjectAltName                          |        emailAddress       |                          Location                         | Type | Size | Digest | Days |
  +----------------------------------+---------------+------------------------------------------------------------------+---------------------------+-----------------------------------------------------------+------+------+--------+------+
  |   lecm-test.distributed-ci.io    |   Generated   |                 DNS:lecm-test.distributed-ci.io                  | distributed-ci@redhat.com |    /etc/letsencrypt/pem/lecm-test.distributed-ci.io.pem   | RSA  | 4096 | sha256 |  89  |
  | lecm-test-test.distributed-ci.io | Not-Generated | DNS;lecm-test-test.distributed-ci.io,DNS:lecm.distributedi-ci.io | distributed-ci@redhat.com | /etc/letsencrypt/pem/lecm-test-test.distributed-ci.io.pem | RSA  | 2048 | sha256 | N/A  |
  +----------------------------------+---------------+------------------------------------------------------------------+---------------------------+-----------------------------------------------------------+------+------+--------+------+


Configuration
-------------

Every parameters are either applicable globally or within the scope of a certificate. The finest specification wins.

+------------------------+----------------+---------+-------------------------------------------------------------------------------+
| Parameter              | Scope          | Default | Description                                                                   |
+========================+================+=========+===============================================================================+
| path                   | global, backup | None    | Foler where will reside all the relevant files                                |
+------------------------+----------------+---------+-------------------------------------------------------------------------------+
| type                   | global, backup | RSA     | Type of the key to generate (Possible: RSA, DSA)                              |
+------------------------+----------------+---------+-------------------------------------------------------------------------------+
| size                   | global, backup | 4096    | Size of the key to generate                                                   |
+------------------------+----------------+---------+-------------------------------------------------------------------------------+
| digest                 | global, backup | sha256  | Digest of the key to generate                                                 |
+------------------------+----------------+---------+-------------------------------------------------------------------------------+
| version                | global, backup | 3       | Version of the SSL Certificate to generate                                    |
+------------------------+----------------+---------+-------------------------------------------------------------------------------+
| subjectAltName         | global, backup | None    | subjectAltName value of the Certificate Signing Request (csr)                 |
+------------------------+----------------+---------+-------------------------------------------------------------------------------+
| countryName            | global, backup | None    | countryName value of the Certificate Signing Request (csr)                    |
+------------------------+----------------+---------+-------------------------------------------------------------------------------+
| stateOrProvinceName    | global, backup | None    | stateOrProvinceName value of the Certificate Signing Request (csr)            |
+------------------------+----------------+---------+-------------------------------------------------------------------------------+
| localityName           | global, backup | None    | localityName value of the Certificate Signing Request (csr)                   |
+------------------------+----------------+---------+-------------------------------------------------------------------------------+
| organizationName       | global, backup | None    | organizationName value of the Certificate Signing Request (csr)               |
+------------------------+----------------+---------+-------------------------------------------------------------------------------+
| organizationalUnitName | global, backup | None    | organizationalUnitName value of the Certificate Signing Request (csr)         |
+------------------------+----------------+---------+-------------------------------------------------------------------------------+
| commonName             | global, backup | None    | commonName value of the Certificate Signing Request (csr)                     |
+------------------------+----------------+---------+-------------------------------------------------------------------------------+
| emailAddress           | global, backup | None    | emailAddress value of the Certificate Signing Request (csr)                   |
+------------------------+----------------+---------+-------------------------------------------------------------------------------+
| account_key_name       | global, backup | None    | Name of the account key to generate                                           |
+------------------------+----------------+---------+-------------------------------------------------------------------------------+
| remaining_days         | global, backup | 10      | Number of days of validity below which the SSL Certificate should be renewed  |
+------------------------+----------------+---------+-------------------------------------------------------------------------------+
| service_name           | global, backup | None    | Service that needs to be reloaded for the change to be taken in consideration |
+------------------------+----------------+---------+-------------------------------------------------------------------------------+


Configuration file example
--------------------------

.. code-block::

  ---
  path: /etc/letsencrypt
  type: RSA
  size: 4096
  digest: sha256
  version: 3
  service_name: httpd
  remaining_days: 10
  emailAddress: admin@example.com
  account_key_name: myhost.key

  certificates:
    my.example.com:
    app.example.com:
      subjectAltName:
        - app.example.com
        - app1.example.com
        - app2.example.com
      emailAddress: app-admin@example.com
      size: 2048
      service_name: nginx


Httpd and Nginx
---------------

``lecm`` does not configure the webservers, they have to be previously
configured to be able to answer the challenges.

httpd
^^^^^

.. code-block::

    Alias /.well-known/acme-challenge /etc/letsencrypt/challenges/my.example.com
    <Directory /etc/letsencrypt/challenges/my.example.com>
        Require all granted
    </Directory>


nginx
^^^^^

.. code-block::

  location /.well-known/acme-challenge/ {
    alias /etc/letsencrypt/challenges/my.example.com;
    try_files $uri =404;
  }


.. |buildstatus| image:: https://img.shields.io/travis/Spredzy/lecm/master.svg
.. _buildstatus: https://travis-ci.org/Spredzy/lecm

.. |release| image:: https://img.shields.io/pypi/v/lecm.svg
.. _release: https://pypi.python.org/pypi/lecm

.. _Let's Encrypt: https://letsencrypt.org/

