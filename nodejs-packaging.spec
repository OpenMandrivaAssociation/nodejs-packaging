Name:           nodejs-packaging
Version:        1
Release:        2
Group:          Development/Other
Summary:        RPM Macros and Utilities for Node.js Packaging
BuildArch:      noarch
License:        MIT
URL:            https://abf.io/dsilakov/nodejs-packaging-rosa
Source0:        %{name}-rosa-%{version}.tar.xz

Requires:       nodejs >= 0.10.12
Requires:       rpm-mandriva-setup-build

%description
This package contains RPM macros and other utilities useful for packaging
Node.js modules and applications in RPM-based distributions.

%prep
%setup -qn %{name}-rosa-%{version}

%build
#nothing to do

%install
install -Dpm0644 macros.nodejs %{buildroot}%{_sysconfdir}/rpm/macros.nodejs
install -Dpm0644 nodejs.attr %{buildroot}%{_rpmhome}/fileattrs/nodejs.attr
install -pm0755 nodejs.prov %{buildroot}%{_rpmhome}/nodejs.prov
install -pm0755 nodejs.req %{buildroot}%{_rpmhome}/nodejs.req
install -pm0755 nodejs-symlink-deps %{buildroot}%{_rpmhome}/nodejs-symlink-deps
install -pm0755 nodejs-fixdep %{buildroot}%{_rpmhome}/nodejs-fixdep
install -Dpm0644 multiver_modules %{buildroot}%{_datadir}/node/multiver_modules

%files
%doc LICENSE
%{_datadir}/node/multiver_modules
%{_sysconfdir}/rpm/macros.nodejs
%{_rpmhome}/fileattrs/nodejs*.attr
%{_rpmhome}/nodejs*
