# For the sake of being able to exchange packages, this
# package is (more or less) kept in sync with the Fedora
# package at https://src.fedoraproject.org/rpms/nodejs-packaging
#
# Please try to remain compatible.
%global macrosdir %(d=%{_rpmconfigdir}/macros.d; [ -d $d ] || d=%{_sysconfdir}/rpm; echo $d)

Name:           nodejs-packaging
Version:	2023.10
Release:	4
Summary:        RPM Macros and Utilities for Node.js Packaging
BuildArch:      noarch
License:        MIT
URL:            https://fedoraproject.org/wiki/Node.js/Packagers
Source0000:	test.tar.zst
Source0001:	https://src.fedoraproject.org/rpms/nodejs-packaging/raw/rawhide/f/LICENSE
Source0002:	https://src.fedoraproject.org/rpms/nodejs-packaging/raw/rawhide/f/README.md
Source0003:	https://src.fedoraproject.org/rpms/nodejs-packaging/raw/rawhide/f/macros.nodejs
Source0004:	https://src.fedoraproject.org/rpms/nodejs-packaging/raw/rawhide/f/multiver_modules
Source0005:	https://src.fedoraproject.org/rpms/nodejs-packaging/raw/rawhide/f/nodejs-fixdep
Source0006:	https://src.fedoraproject.org/rpms/nodejs-packaging/raw/rawhide/f/nodejs-setversion
Source0007:	https://src.fedoraproject.org/rpms/nodejs-packaging/raw/rawhide/f/nodejs-symlink-deps
Source0008:	https://src.fedoraproject.org/rpms/nodejs-packaging/raw/rawhide/f/nodejs.attr
Source0009:	https://src.fedoraproject.org/rpms/nodejs-packaging/raw/rawhide/f/nodejs.prov
Source0010:	https://src.fedoraproject.org/rpms/nodejs-packaging/raw/rawhide/f/nodejs.req
Source0011:	https://src.fedoraproject.org/rpms/nodejs-packaging/raw/rawhide/f/nodejs-packaging-bundler
Patch0:		https://src.fedoraproject.org/rpms/nodejs-packaging/pull-request/7.patch
BuildRequires:  python3

#nodejs-devel before 0.10.12 provided these macros and owned /usr/share/node
Requires:       nodejs
Requires:       rpm-openmandriva-setup-build

%description
This package contains RPM macros and other utilities useful for packaging
Node.js modules and applications in RPM-based distributions.

%package bundler
Summary:	Bundle a node.js application dependencies
Requires:	npm
Requires:	coreutils, findutils, jq
 
%description bundler
nodejs-packaging-bundler bundles a node.js application node_module dependencies
It gathers the application tarball.
It generates a runtime (prod) tarball with runtime node_module dependencies
It generates a testing (dev) tarball with node_module dependencies for testing
It generates a bundled license file that gets the licenses in the runtime
dependency tarball

%prep
cp -a %{S:1} %{S:2} %{S:3} %{S:4} %{S:5} %{S:6} %{S:7} %{S:8} %{S:9} %{S:10} %{S:11} .
chmod +x *.prov *.req
tar xf %{S:0}
%autopatch -p1

%build

%install
install -Dpm0644 macros.nodejs %{buildroot}%{macrosdir}/macros.nodejs
install -Dpm0644 nodejs.attr %{buildroot}%{_rpmconfigdir}/fileattrs/nodejs.attr
install -pm0755 nodejs.prov %{buildroot}%{_rpmconfigdir}/nodejs.prov
install -pm0755 nodejs.req %{buildroot}%{_rpmconfigdir}/nodejs.req
install -pm0755 nodejs-symlink-deps %{buildroot}%{_rpmconfigdir}/nodejs-symlink-deps
install -pm0755 nodejs-fixdep %{buildroot}%{_rpmconfigdir}/nodejs-fixdep
install -pm0755 nodejs-setversion %{buildroot}%{_rpmconfigdir}/nodejs-setversion
install -Dpm0644 multiver_modules %{buildroot}%{_datadir}/node/multiver_modules
install -Dpm0755 nodejs-packaging-bundler %{buildroot}%{_bindir}/nodejs-packaging-bundler

%check
./test/run

%files
%license LICENSE
%{macrosdir}/macros.nodejs
%{_rpmconfigdir}/fileattrs/nodejs*.attr
%{_rpmconfigdir}/nodejs*
%{_datadir}/node/multiver_modules

%files bundler
%{_bindir}/nodejs-packaging-bundler
