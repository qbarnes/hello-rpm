# Introduction

You can build a "Hello, World" rpm either with the native tools or
with `mock` using these walk-through instructions.

Keep in mind when this program builds, that it is no ordinary
"Hello, World" program.  It's a "Hello, World" program on steroids.
It even has internationalization support.

The walk-through below is for illustrative and educational use only.
These steps are not necessarily how such a process would be advised
for general development use.

For further information on `mock`, see:
https://github.com/rpm-software-management/mock/wiki

# Building RPMs Natively

Prep your system with the necessary packages:
```
$ sudo yum install -y git yum-utils rpmdevtools rpm-build gcc make
```

Prep your home directory area for building RPMs:
```
$ rpmdev-setuptree
$ ls -l .rpmmacros rpmbuild
```

Clone the "Hello, World" repository and change to the SPECS directory:
```
$ git clone git@github.com:qbarnes/hello-rpm.git
$ cd hello-rpm/SPECS
```

Install the packages needed to build the Source RPM (all may already be
installed):
```
$ sudo yum-builddep -y hello.spec
```

Download the "Hello, World" tarball into your `%{_sourcedir}` directory
(typically `~/rpmbuild/SOURCES`):
```
$ spectool -g -R hello.spec
```

Now to build the binary RPMs into your `%{_topdir}/RPMS/*` directories
(typically `~/rpmbuild/RPMS/*`):
```
$ rpmbuild -bb hello.spec
```

The RPMs can be viewed with:
```
$ ls -l $(rpm -E '%{_topdir}')/RPMS/$(arch)/hello*.rpm
```

# Building RPMs Using Mock

Prep your system with the necessary packages:
```
$ sudo yum install -y git yum-utils rpmdevtools
```

Now install `mock`.  You'll first need to install the EPEL yum
repository file.  See https://fedoraproject.org/wiki/EPEL

Now install `mock`:
```
$ sudo yum install -y --enablerepo=epel mock
```

And add yourself to the `mock` user group:
```
$ sudo usermod -G mock "$USER"
```

You don't _have_ to add yourself to the `mock` user group.  If you
don't, you'll have to run `mock` below using `sudo`.

**Before continuing, you'll need to log out and log back in to update your
credentials.**

Clone the "Hello, World" repository:
```
$ git clone git@github.com:qbarnes/hello-rpm.git
```

Change to the `hello-rpm` directory and prep it:
```
$ cd hello-rpm
$ sudo yum-builddep -y SPECS/hello.spec
$ mkdir SOURCES
$ spectool -g -C SOURCES SPECS/hello.spec
```

The first time you run `mock`, it'll take much longer than other
runs because it has to download and cache the upstream yum
repository data and necessary rpms.

Change back into the git work area and build a source RPM:
```
$ cd hello-rpm
$ mock -r epel-8-$(arch) \
    --resultdir=results_srpm \
    --buildsrpm \
    --spec SPECS/hello.spec --sources SOURCES
```

Look under `results_srpm` to see your new srpm and log files from its build:
```
$ ls -l results_srpm
```

Let's now build the binary RPMs:
```
$ mock -r epel-8-$(arch) \
    --resultdir=results_rpms \
    --rebuild results_srpm/hello-2.10-1.*.src.rpm
```

Look under `results_rpms`.  You'll see not only the binary rpms, but
a new `hello-2.10-1.*.src.rpm` too.  This is because the source rpm
got rebuilt before its binary RPMs.  That's because you might have
for example taken a source rpm from anywhere (e.g. one from RHEL 6
or Fedora 31).  This new source rpm would be for the target system.
```
$ ls -l results_rpms
```

With `mock`, you don't have to build RPMs just for the host OS
you're on.  You can build other OSes too.  Note though, don't go
"forward" (e.g. trying to build RHEL 8 RPMs using a RHEL 7 host).
It may "work" sometimes, but that'll just be dumb luck if it does.

For example, to make RHEL 6 "Hello, World" RPMs by using the
source RPM first built above, run:
```
$ mock -r epel-6-$(arch) \
    --resultdir=results_el6_rpms \
    --rebuild results_srpm/hello-2.10-1.*.src.rpm
$ ls -l results_el6_rpms
```

For those wanting to know what's beyond `mock`, you may want to
read about
* [Tito](https://github.com/rpm-software-management/tito/blob/master/README.md) - A tool for managing RPM based projects using git for their source code repositories
* [Koji](https://fedoraproject.org/wiki/Koji) - A tool for building trees of RPMs
* [COPR](https://developer.fedoraproject.org/deployment/copr/about.html) and [Open Build Service](https://openbuildservice.org/) - Package build service engines
