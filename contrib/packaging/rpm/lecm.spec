%global srcname lecm

Name:           %{srcname}
Version:        0.0.4
Release:        1%{?dist}

Summary:        Let's Encrypt Certificate Manager
License:        ASL 2.0
URL:            http://pypi.python.org/pypi/%{srcname}
Source0:        http://pypi.python.org/packages/source/l/%{srcname}/%{srcname}-%{version}.tar.gz


BuildArch:      noarch

BuildRequires:  python2-devel

Requires:       python-prettytable
Requires:       PyYAML
Requires:       python-requests
Requires:       pyOpenSSL

%description
Let's Encrypt Certificate Manager is an utility to ease the management
and renewal of Let's Encrypt SSL certificates.

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


%prep
%autosetup -n %{srcname}-%{version}

%build
%py2_build
%py3_build


%install
%py2_install
%py3_install


%files
%doc README.rst
%{python2_sitelib}/%{srcname}
%{python2_sitelib}/*.egg-info
%{_bindir}/lecm

%files -n python3-%{srcname}
%doc README.rst
%{python3_sitelib}/%{srcname}
%{python3_sitelib}/*.egg-info
%{_bindir}/lecm

%changelog
* Wed Sep 28 2016 Yanis Guenane <yguenane@redhat.com> 0.0.4-1
- Initial commit
