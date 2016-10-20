%global srcname lecm

%if 0%{?fedora}
%global with_python3 1
%endif

Name:           %{srcname}
Version:        0.0.5
Release:        1%{?dist}

Summary:        Let's Encrypt Certificate Manager
License:        ASL 2.0
URL:            http://pypi.python.org/pypi/%{srcname}
Source0:        http://pypi.python.org/packages/source/l/%{srcname}/%{srcname}-%{version}.tar.gz


BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-setuptools

Requires:       python-prettytable
Requires:       PyYAML
Requires:       python-requests
Requires:       pyOpenSSL

%description
Let's Encrypt Certificate Manager is an utility to ease the management
and renewal of Let's Encrypt SSL certificates.

%if 0%{?with_python3}
%package -n python3-%{srcname}
Summary:        Let's Encrypt Certificate Manager

BuildRequires:  python3-devel

Requires:       python3-prettytable
Requires:       python3-PyYAML
Requires:       python3-requests
Requires:       python3-pyOpenSSL

%description -n python3-%{srcname}
Let's Encrypt Certificate Manager is an utility to ease the management
and renewal of Let's Encrypt SSL certificates.
%endif


%prep
%autosetup -n %{srcname}-%{version}

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif


%install
%py2_install
%if 0%{?with_python3}
%py3_install
%endif


%files
%doc README.rst
%{python2_sitelib}/%{srcname}
%{python2_sitelib}/*.egg-info
%{_bindir}/lecm

%if 0%{?with_python3}
%files -n python3-%{srcname}
%doc README.rst
%{python3_sitelib}/%{srcname}
%{python3_sitelib}/*.egg-info
%{_bindir}/lecm
%endif

%changelog
* Thu Oct 27 2016 Yanis Guenane <yguenane@redhat.com> 0.0.5-1
- Deb and Rpm packaging
- Reload service only when necessary #29
- Add more sample to show how lecm address different situation #28
- Enforce proper SELinux context on generated files #25
- Have a default value for account_key_name #23

* Wed Sep 28 2016 Yanis Guenane <yguenane@redhat.com> 0.0.4-1
- Initial commit
