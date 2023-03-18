# https://fedoraproject.org/wiki/How_to_create_a_GNU_Hello_RPM_package

Name:           hello
Version:        2.12.1
Release:        1%{?dist}
Summary:        The "Hello World" program from GNU

License:        GPLv3+
URL:            http://ftp.gnu.org/gnu/%{name}
Source0:        http://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.gz

BuildRequires: gcc
BuildRequires: gettext
      
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description 
The "Hello World" program, done with all bells and whistles of a proper FOSS 
project, including configuration, build, internationalization, help files, etc.

%prep
%autosetup

%build
%configure
%{__make} %{?_smp_mflags}

%install
%make_install
%find_lang %{name}
%{__rm} -f %{buildroot}/%{_infodir}/dir

%post
/sbin/install-info %{_infodir}/%{name}.info %{_infodir}/dir || :

%preun
if [ $1 = 0 ] ; then
/sbin/install-info --delete %{_infodir}/%{name}.info %{_infodir}/dir || :
fi

%files -f %{name}.lang
%{_mandir}/man1/hello.1.gz
%{_infodir}/%{name}.info.gz
%{_bindir}/hello

#%doc
#AUTHORS ChangeLog COPYING NEWS README THANKS TODO

%changelog
* Sat Mar 18 2023 Quentin Barnes <qbarnes@gmail.com> 2.12.1-1
- Update to version 2.12.1.

* Wed Jul 27 2016 Quentin Barnes <qbarnes@yahoo-inc.com> 2.10-1
- Change spec file to reference command rather than a package name.
- Update to version 2.10.

* Tue Sep 06 2011 The Coon of Ty <Ty@coon.org> 2.8-1
- Initial version of the package
