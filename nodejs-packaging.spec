Name:           nodejs-packaging
Version:        1
Release:        5
Group:          Development/Other
Summary:        RPM Macros and Utilities for Node.js Packaging
BuildArch:      noarch
License:        MIT
URL:            https://abf.io/dsilakov/nodejs-packaging-rosa
Source0:        %{name}-rosa-%{version}.tar.xz

# For 2to3
BuildRequires:	python

Requires:       nodejs >= 0.10.12
Requires:       rpm-mandriva-setup-build

%description
This package contains RPM macros and other utilities useful for packaging
Node.js modules and applications in RPM-based distributions.

%prep
%setup -qn %{name}-rosa-%{version}

%build
2to3 -w nodejs.prov
2to3 -w nodejs.req
2to3 -w nodejs-symlink-deps
2to3 -w nodejs-fixdep
rm -f *.bak

%install
install -Dpm0644 nodejs.macros %{buildroot}%{_sysconfdir}/rpm/macros.nodejs
install -Dpm0755 nodejs.prov %{buildroot}%{_rpmhome}/nodejs.prov
install -Dpm0755 nodejs.req %{buildroot}%{_rpmhome}/nodejs.req
install -Dpm0755 nodejs-symlink-deps %{buildroot}%{_rpmhome}/nodejs-symlink-deps
install -Dpm0755 nodejs-fixdep %{buildroot}%{_rpmhome}/nodejs-fixdep
install -Dpm0644 multiver_modules %{buildroot}%{_datadir}/node/multiver_modules

%files
%doc LICENSE
%{_datadir}/node/multiver_modules
%{_sysconfdir}/rpm/macros.nodejs
%{_rpmhome}/nodejs*
