%global srcname lecm

Name:           %{srcname}
Version:        0.0.6
Release:        1%{?dist}

Summary:        Let's Encrypt Certificate Manager
License:        ASL 2.0
URL:            http://pypi.python.org/pypi/%{srcname}
Source0:        http://pypi.python.org/packages/source/l/%{srcname}/%{srcname}-%{version}.tar.gz
Source1:        lecm.cron
Source2:        lecm.1.gz


BuildArch:      noarch

BuildRequires:  python3-devel

Requires:       acme-tiny
Requires:       python3-prettytable
Requires:       python3-PyYAML
Requires:       python3-requests
Requires:       python3-pyOpenSSL

%description
Let's Encrypt Certificate Manager is an utility to ease the management
and renewal of Let's Encrypt SSL certificates.


%prep
%autosetup -n %{srcname}-%{version}
# NOTE(spredzy): We need to kee acme-tiny in the requirements in the tarball
# for user to still be able to use it fully from pip install, but the acme-tiny
# package does not install a python module but just the independant script. Hence
# the need for the sed command below.
sed -i '/acme-tiny/d' requirements.txt


%build
%py3_build


%install
%py3_install

mkdir -p %{buildroot}%{_sysconfdir}/cron.d/
install -p -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/cron.d/lecm

mkdir -p %{buildroot}%{_mandir}/man1/
install -p -m 0644 %{SOURCE2} %{buildroot}%{_mandir}/man1/lecm.1.gz

mkdir -p %{buildroot}%{_datadir}/%{srcname}/sample/
install -p -m 0644 sample/*.conf %{buildroot}%{_datadir}/%{srcname}/sample/


%files
%doc README.rst
%{python3_sitelib}/%{srcname}
%{python3_sitelib}/*.egg-info
%{_bindir}/%{srcname}
%{_datadir}/%{srcname}
%{_mandir}/man1/%{srcname}.1.gz
%config(noreplace) %{_sysconfdir}/cron.d/%{srcname}

%changelog

* Wed Nov 09 2016 Yanis Guenane <yguenane@redhat.com> 0.0.6-1
- doc: Added instal. documentation (pypi/debian) #37
- Print USAGE message when no parameter has been passed #43
- certificates: Allow one to use Let's Encrypt staging API #42
- setup.py: Fix url and add Python 3.5 support #41
- Travis: Add check for Python 3.5 #39
- certificates: Allow one to reload multiple service #38
- Fix mistake in the alias statement #36

* Thu Oct 27 2016 Yanis Guenane <yguenane@redhat.com> 0.0.5-1
- Deb and Rpm packaging
- Reload service only when necessary #29
- Add more sample to show how lecm address different situation #28
- Enforce proper SELinux context on generated files #25
- Have a default value for account_key_name #23

* Wed Sep 28 2016 Yanis Guenane <yguenane@redhat.com> 0.0.4-1
- Initial commit
