========================================
lecm: Let's Encrypt Certificates Manager
========================================

|buildstatus|_ |release|_ |versions|_


`Let's Encrypt`_ Certificates Manager (lecm) is an
utility that allows one to manage (generate and renew) Let's Encrypt SSL
certificates.

Goal
----

The goal of ``lecm`` is to be able to generate and renew
`Let's Encrypt`_  SSL certificates automatically.

``lecm`` is configuration driven. Each certificate that needs to be managed
is described in the configuration file.

Installation
------------

Using pypi
^^^^^^^^^^

You just need to

``$ pip install lecm``

Debian-based distro (Debian, Ubuntu, …)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There is an `official Debian package for lecm`_

``$ sudo apt-get install lecm``

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
if its expiry date is lower than the ``remaining_days`` value.


``--force``
^^^^^^^^^^^

``lecm --force`` will force the regeneration or renewal of SSL certificates, even
if its expiry date is not lower than the ``remainin_days`` value.


``--list``
^^^^^^^^^^

``lecm --list`` will display basic informations about currently configured items.


.. code-block::

 +--------- +----------------------------------+---------------+------------------------------------------------------------------+-----------------------------------------------------------+------+
 |  In Sync |               Item               |     Status    |                          subjectAltName                          |                          Location                         | Days |
 +--------- +----------------------------------+---------------+------------------------------------------------------------------+-----------------------------------------------------------+------+
 |  True    |   lecm-test.distributed-ci.io    |   Generated   |                 DNS:lecm-test.distributed-ci.io                  |    /etc/letsencrypt/pem/lecm-test.distributed-ci.io.pem   |  89  |
 |  False   | lecm-test-test.distributed-ci.io | Not-Generated | DNS;lecm-test-test.distributed-ci.io,DNS:lecm.distributedi-ci.io | /etc/letsencrypt/pem/lecm-test-test.distributed-ci.io.pem | N/A  |
 +----------+----------------------------------+---------------+------------------------------------------------------------------+-----------------------------------------------------------+------+


``--list-details``
^^^^^^^^^^^^^^^^^^

``lecm --list-details`` will display details informations about currently configured items.

.. code-block::

  +--------- +----------------------------------+---------------+------------------------------------------------------------------+---------------------------+--------------+-----------------------------------------------------------+------+------+--------+------+
  |  In Sync |               Item               |     Status    |                          subjectAltName                          |        emailAddress       |  Environment |                          Location                         | Type | Size | Digest | Days |
  +--------- +----------------------------------+---------------+------------------------------------------------------------------+---------------------------+--------------+-----------------------------------------------------------+------+------+--------+------+
  |  True    |   lecm-test.distributed-ci.io    |   Generated   |                 DNS:lecm-test.distributed-ci.io                  | distributed-ci@redhat.com |  production  |    /etc/letsencrypt/pem/lecm-test.distributed-ci.io.pem   | RSA  | 4096 | sha256 |  89  |
  |  False   | lecm-test-test.distributed-ci.io | Not-Generated | DNS;lecm-test-test.distributed-ci.io,DNS:lecm.distributedi-ci.io | distributed-ci@redhat.com |    staging   | /etc/letsencrypt/pem/lecm-test-test.distributed-ci.io.pem | RSA  | 2048 | sha256 | N/A  |
  +----------+----------------------------------+---------------+------------------------------------------------------------------+---------------------------+--------------|-----------------------------------------------------------+------+------+--------+------+


Configuration
-------------

Every parameters are either applicable globally or within the scope of a certificate. The finest specification wins.

+------------------------+---------------------+-------------------+-------------------------------------------------------------------------------+
| Parameter              | Scope               | Default           | Description                                                                   |
+========================+=====================+===================+===============================================================================+
| path                   | global, certificate | None              | Folder where will reside all the relevant files                               |
+------------------------+---------------------+-------------------+-------------------------------------------------------------------------------+
| type                   | global, certificate | RSA               | Type of the key to generate (Possible: RSA, DSA)                              |
+------------------------+---------------------+-------------------+-------------------------------------------------------------------------------+
| size                   | global, certificate | 4096              | Size of the key to generate                                                   |
+------------------------+---------------------+-------------------+-------------------------------------------------------------------------------+
| digest                 | global, certificate | sha256            | Digest of the key to generate                                                 |
+------------------------+---------------------+-------------------+-------------------------------------------------------------------------------+
| version                | global, certificate | 3                 | Version of the SSL Certificate to generate                                    |
+------------------------+---------------------+-------------------+-------------------------------------------------------------------------------+
| subjectAltName         | global, certificate | None              | subjectAltName value of the Certificate Signing Request (csr)                 |
+------------------------+---------------------+-------------------+-------------------------------------------------------------------------------+
| countryName            | global, certificate | None              | countryName value of the Certificate Signing Request (csr)                    |
+------------------------+---------------------+-------------------+-------------------------------------------------------------------------------+
| stateOrProvinceName    | global, certificate | None              | stateOrProvinceName value of the Certificate Signing Request (csr)            |
+------------------------+---------------------+-------------------+-------------------------------------------------------------------------------+
| localityName           | global, certificate | None              | localityName value of the Certificate Signing Request (csr)                   |
+------------------------+---------------------+-------------------+-------------------------------------------------------------------------------+
| organizationName       | global, certificate | None              | organizationName value of the Certificate Signing Request (csr)               |
+------------------------+---------------------+-------------------+-------------------------------------------------------------------------------+
| organizationalUnitName | global, certificate | None              | organizationalUnitName value of the Certificate Signing Request (csr)         |
+------------------------+---------------------+-------------------+-------------------------------------------------------------------------------+
| commonName             | global, certificate | None              | commonName value of the Certificate Signing Request (csr)                     |
+------------------------+---------------------+-------------------+-------------------------------------------------------------------------------+
| emailAddress           | global, certificate | None              | emailAddress value of the Certificate Signing Request (csr)                   |
+------------------------+---------------------+-------------------+-------------------------------------------------------------------------------+
| account_key_name       | global, certificate | account_$fqdn.key | Name of the account key to generate                                           |
+------------------------+---------------------+-------------------+-------------------------------------------------------------------------------+
| remaining_days         | global, certificate | 10                | Number of days of validity below which the SSL Certificate should be renewed  |
+------------------------+---------------------+-------------------+-------------------------------------------------------------------------------+
| service_name           | global, certificate | httpd             | Service that needs to be reloaded for the change to be taken in consideration |
+------------------------+---------------------+-------------------+-------------------------------------------------------------------------------+
| service_provider       | global, certificate | systemd           | Service management system (Possible: systemd, sysv)                           |
+------------------------+---------------------+-------------------+-------------------------------------------------------------------------------+
| environment            | global, certificate | production        | Let's Encrypt environment to use (Possible: production, staging)              |
+------------------------+---------------------+-------------------+-------------------------------------------------------------------------------+


Configuration file example
--------------------------

.. code-block::

  ---
  path: /etc/letsencrypt

  certificates:
    my.example.com:
    app.example.com:
      subjectAltName:
        - app.example.com
        - app1.example.com
        - app2.example.com

More example can be found in the ``sample/`` directory.

Httpd and Nginx
---------------

``lecm`` does not configure the webservers, they have to be previously
configured to be able to answer the challenges. NOTE: Let's
Encrypt will perform a plain HTTP request to port 80 on your server, so you
must serve the challenge files via HTTP. See the HTTP Challenge section
of the `ACME specification`_ for more details.

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
    alias /etc/letsencrypt/challenges/my.example.com/;
    try_files $uri =404;
  }


.. |buildstatus| image:: https://img.shields.io/travis/Spredzy/lecm/master.svg
.. _buildstatus: https://travis-ci.org/Spredzy/lecm

.. |release| image:: https://img.shields.io/pypi/v/lecm.svg
.. _release: https://pypi.python.org/pypi/lecm

.. |versions| image:: https://img.shields.io/pypi/pyversions/lecm.svg
.. _versions: https://pypi.python.org/pypi/lecm

.. _Let's Encrypt: https://letsencrypt.org/
.. _official Debian package for lecm: https://tracker.debian.org/pkg/lecm
.. _ACME specification: https://tools.ietf.org/html/draft-ietf-acme-acme-07#section-8.3
