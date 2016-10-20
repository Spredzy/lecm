% LECM(1) Let's Encrypt Manager manual
% Yanis Guenane
% October 17, 2016
% pandoc -s -t man lecm.md -o lecm.1

# NAME

lecm - Let's Encrypt Manager

# SYNOPSIS

lecm [*options*]

# DESCRIPTION

Let's Encrypt Certificates Manager (lecm) is an utility that allows one to
manage (generate and renew) Let's Encrypt SSL certificates.

list all certificates managed by lecm

    lecm -l

renew all certificates managed by lecm, according */etc/lecm.conf*

    lecm --renew

# OPTIONS

-h, \--help
:   Show this help message and exit

-v, \--version
:   Show program's version number and exit

\--debug
:   Display DEBUG information level

\--noop
:   Proceed in noop mode

\--conf *CONF*
:   Path to configuration file

\--items *[ITEMS [ITEMS ...]]*
:   Limit the item to apply the action to

-l, \--list
:   List the lecm configured certificates

-ld, \--list-details
:   List the lecm configured certificates(details)

\--generate
:   Generate Lets Encrypt SSL Certificates

\--renew
:   Renew already generated SSL Certificates

# SEE ALSO

The lecm source code and all documentation may be downloaded from
<https://github.com/Spredzy/lecm>.
