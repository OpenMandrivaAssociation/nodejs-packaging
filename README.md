# How to update Node.js in Fedora

## Determine the Node.js version
Monitor the [Node.js Blog](https://nodejs.org/en/blog/) to be notified of
available updates.

For simplicity and copy-and-paste of instructions below, set some variables
here:

```
NODEJS_MAJOR=12
NODEJS_VERSION=12.9.0
```

## Clone the Fedora package repository
These steps assume that you are a comaintainer of Node.js or a provenpackager
in Fedora.

```
fedpkg clone nodejs nodejs-fedora
```

Next, switch to the major version branch you are going to update. We'll use
Node.js 12.9.0 in this document. Adjust the versions appropriately for the
version you are working on.

```
pushd nodejs-fedora
fedpkg switch-branch $NODEJS_MAJOR
popd
```


## Clone the Fedora Module repository

```
fedpkg clone modules/nodejs nodejs-fedora-module
```


## Clone the upstream Node.js repository
```
git clone -o upstream git://github.com/nodejs/node.git nodejs-upstream
```


## Rebase the Fedora patches atop the latest release

```
pushd nodejs-upstream
git checkout -b fedora-v$NODEJS_VERSION v$NODEJS_VERSION
git am -3 ../nodejs-fedora/*.patch
```

If the patches do not apply cleanly, resolve the merges appropriately. Once
they have all been applied, output them again:

```
git format-patch -M --patience --full-index -o ../nodejs-fedora v$NODEJS_VERSION..HEAD
popd
```


## Update the Node.js tarball and specfile

```
pushd nodejs-fedora
./nodejs-tarball.sh $NODEJS_VERSION
```

Note that this command will also output all of the versions for the software
bundled with Node.js. You will need to edit `nodejs.spec` and update the
%global values near the top of that file to include the appropriate values
matching the dependencies. Make sure to also update the Node.js versions too!

Note that if libuv is updated, you need to ensure that the libuv in each
buildroot is of a sufficient version. If not, you may need to update that
package first and submit a buildroot override.

Update the RPM spec %changelog appropriately.


## (Preferred) Perform a scratch-build on at least one architecture

```
fedpkg scratch-build [--arch x86_64] --srpm
```

Verify that it built successfully.


## Push the changes up to Fedora
```
fedpkg commit -cs
fedpkg push
popd
```


## (Optional) Build for Fedora releases

If this major version is the default for one or more Fedora releases, build it
for them. (Note: this step will go away in the future, once module default
streams are available in the non-modular buildroot.)

In the case of Node.js 12.x, this is the default version for Fedora 31 and 32.

```
pushd nodejs-fedora
fedpkg switch-branch [master|31]
git merge $NODEJS_MAJOR
fedpkg push
fedpkg build
popd
```

## Build module stream

```
pushd nodejs-fedora-module
fedpkg switch-branch $NODEJS_MAJOR
```

If the module has changed any package dependencies (such as added a dep on a
new shared library), you may need to modify nodejs.yaml here. If not, you can
simply run:

```
git commit --allow-empty -sm "Update to $NODEJS_VERSION"
fedpkg push
fedpkg module-build
popd
```

## Submit built packages to Bodhi
Follow the usual processes for stable/branched releases to submit builds for
testing.


# How to bundle nodejs libraries in Fedora

The upstream Node.js stance on 
[global library packages](https://nodejs.org/en/blog/npm/npm-1-0-global-vs-local-installation/) 
is that they are ".. best avoided if not needed."  In Fedora, we take the same 
stance with our nodejs packages.  You can provide a package that uses nodejs, 
but you should bundle all the nodejs libraries that are needed.

We are providing a sample spec file and bundling script here.  
For more detailed packaging information go to the 
[Fedora Node.js Packaging Guildelines](https://docs.fedoraproject.org/en-US/packaging-guidelines/Node.js/)

## Bundling Script

```
nodejs-packaging-bundler <npm_name> [version]
```

nodejs-packaging-bundler is it's own package, nodejs-packaging-bundler and must be installed before use.  
nodejs-packaging-bundler gets the latest npm version available, if no version is given.  
It produces four files and puts them in ${HOME}/rpmbuild/SOURCES

 * <npm_name>-<version>.tgz - This is the tarball from npm.org
 * <npm_name>-<version>-nm-prod.tgz - This is the tarball that contains all the bundled nodejs modules <npm_name> needs to run
 * <npm_name>-<version>-nm-dev.tgz - This is the tarball that contains all the bundled nodejs modules <npm_name> needs to test
 * <npm_name>-<version>-bundled-licenses.txt - This lists the bundled licenses in <npm_name>-<version>-nm-prod.tgz

## Sample Spec File

```
%global npm_name my_nodejs_application
...
License:  <license1> and <license2> and <license3>
...
Source0:  http://registry.npmjs.org/%{npm_name}/-/%{npm_name}-%{version}.tgz
Source1:  %{npm_name}-%{version}-nm-prod.tgz
Source2:  %{npm_name}-%{version}-nm-dev.tgz
Source3:  %{npm_name}-%{version}-bundled-licenses.txt
...
BuildRequires: nodejs-devel
...
%prep
%setup -q -n package
cp %{SOURCE3} .
...
%build
# Setup bundled node modules
tar xfz %{SOURCE1}
mkdir -p node_modules
pushd node_modules
ln -s ../node_modules_prod/* .
ln -s ../node_modules_prod/.bin .
popd
...
%install
mkdir -p %{buildroot}%{nodejs_sitelib}/%{npm_name}
cp -pr index.js lib package.json %{buildroot}%{nodejs_sitelib}/%{npm_name}
# Copy over bundled nodejs modules
cp -pr node_modules node_modules_prod %{buildroot}%{nodejs_sitelib}/%{npm_name}
...
%check
%nodejs_symlink_deps --check
# Setup bundled dev node_modules for testing
tar xfz %{SOURCE2}
pushd node_modules
ln -s ../node_modules_dev/* .
popd
pushd node_modules/.bin
ln -s ../../node_modules_dev/.bin/* .
popd
# Example test run using the binary in ./node_modules/.bin/
./node_modules/.bin/vows --spec --isolate
...
%files
%doc HISTORY.md
%license LICENSE.md %{npm_name}-%{version}-bundled-licenses.txt
%{nodejs_sitelib}/%{npm_name}
```

