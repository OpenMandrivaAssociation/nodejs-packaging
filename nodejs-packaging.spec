%global macrosdir %(d=%{_rpmconfigdir}/macros.d; [ -d $d ] || d=%{_sysconfdir}/rpm; echo $d)

Name:           nodejs-packaging
Version:	25
Release:	1
Summary:        RPM Macros and Utilities for Node.js Packaging
BuildArch:      noarch
License:        MIT
URL:            https://fedoraproject.org/wiki/Node.js/Packagers
Source0:        https://releases.pagure.org/%{name}/%{name}-fedora-%{version}.tar.xz
#ExclusiveArch:  %{nodejs_arches} noarch

BuildRequires:  python3

#nodejs-devel before 0.10.12 provided these macros and owned /usr/share/node
Requires:       nodejs(engine) >= 0.10.12
Requires:       rpm-openmandriva-setup-build

%description
This package contains RPM macros and other utilities useful for packaging
Node.js modules and applications in RPM-based distributions.


%prep
%autosetup -p 1 -n %{name}-fedora-%{version}


%build
2to3 -w nodejs.prov
2to3 -w nodejs.req
2to3 -w nodejs-symlink-deps
2to3 -w nodejs-fixdep
rm -f *.bak
#nothing to do


%install
install -Dpm0644 macros.nodejs %{buildroot}%{macrosdir}/macros.nodejs
install -Dpm0644 nodejs.attr %{buildroot}%{_rpmconfigdir}/fileattrs/nodejs.attr
install -pm0755 nodejs.prov %{buildroot}%{_rpmconfigdir}/nodejs.prov
install -pm0755 nodejs.req %{buildroot}%{_rpmconfigdir}/nodejs.req
install -pm0755 nodejs-symlink-deps %{buildroot}%{_rpmconfigdir}/nodejs-symlink-deps
install -pm0755 nodejs-fixdep %{buildroot}%{_rpmconfigdir}/nodejs-fixdep
install -pm0755 nodejs-setversion %{buildroot}%{_rpmconfigdir}/nodejs-setversion
install -Dpm0644 multiver_modules %{buildroot}%{_datadir}/node/multiver_modules


%check
./test/run


%files
%license LICENSE
%{macrosdir}/macros.nodejs
%{_rpmconfigdir}/fileattrs/nodejs*.attr
%{_rpmconfigdir}/nodejs*
%{_datadir}/node/multiver_modules
