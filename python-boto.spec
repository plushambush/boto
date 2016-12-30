%if 0%{?rhel} && 0%{?rhel} <= 6
%{!?__python2: %global __python2 /usr/bin/python2}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%endif

%define pkgname boto
%define buildid %{nil}

Summary:        A simple lightweight interface to Amazon Web Services
Name:           python-%{pkgname}
Version:        2.12.0
Release:        CROC8%{?buildid}%{?dist}
Epoch:          1441065600

Group:          Development/Languages
License:        MIT
URL:            http://github.com/C2Devel/boto
Source0:        %{pkgname}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-setuptools

Provides:       %name = %version-%release

%description
Boto is a Python package that provides interfaces to Amazon Web Services.
It supports S3 (Simple Storage Service), SQS (Simple Queue Service) via
the REST API's provided by those services and EC2 (Elastic Compute Cloud)
via the Query API. The goal of boto is to provide a very simple, easy to
use, lightweight wrapper around the Amazon services.

%prep
%setup -q -n %{pkgname}-%{version}

%build
%{__python2} setup.py build

%install
[ "%buildroot" = "/" ] || rm -rf "%buildroot"

%{__python2} setup.py install -O1 \
    --skip-build \
    --root "%buildroot" \
    --install-lib="%{python2_sitelib}"

%files
%defattr(-,root,root,-)
%doc README.rst
%{_bindir}/*
%{python2_sitelib}/*

%clean
[ "%buildroot" = "/" ] || rm -rf "%buildroot"

%changelog
* Fri Dec 30 2016 Mikhail Ushanov <gm.mephisto@gmail.com> - 2.12.0-8
- Fix unittest
- vpc: remove AZ field from vpcs api

* Wed Jun 22 2016 Mikhail Ushanov <gm.mephisto@gmail.com> - 2.12.0-7
- EC2: remove tiers
- Add availability zone argument to describe_account_attribute

* Mon Apr 04 2016 Mikhail Ushanov <gm.mephisto@gmail.com> - 2.12.0-6
- ec2: remove 'snapshot_instance' c2-specific API method
- Fixed a date bug in the trim_snapshots tests.
- Added targets for building rpms in copr

* Fri Feb 12 2016 Mikhail Ushanov <gm.mephisto@gmail.com> - 2.12.0-5
- Added VPC description field
- Changed travis-ci build to container-based

* Mon Oct 12 2015 Vadim Radovel <vadim@radovel.ru> - 2.12.0-4
- Added Import/Export API.
- Shortcuts for connect to s3 and vpc endpoints.

* Thu Sep 17 2015 Mikhail Ushanov <gm.mephisto@gmail.com> - 2.12.0-3
- Added 'connect_cloudwatch_endpoint' function
- 'NoDevice' option moved from 'EBS' to 'BlockDeviceMapping'
- makefile: ability to build develop rpm package

* Wed Aug 19 2015 Mikhail Ushanov <gm.mephisto@gmail.com> - 2.12.0-2
- Fix duplicate private_ip_address field
- Restore 'epoch' field for overriding default python-boto package

* Thu Jul 23 2015 Mikhail Ushanov <gm.mephisto@gmail.com> - 2.12.0-1
- Updated to 2.12.0.
- Cleanup RPM spec, removed 'epoch' field.
- Added volume attribute 'Iops'.
- Fix VolumeAttribute bool attrs.

* Fri Jul 03 2015 Vadim Radovel <vadim@radovel.ru> - 2.4.1-14
- https unverified for python 2.7.9

* Tue Jan 13 2015 Mikhail Ushanov <gm.mephisto@gmail.com> - 2.4.1-13
- Added field private_ip_address into response.
- Added 'get_vpc_attribute' and 'modify_vpc_attribute' methods.
- DetachVirtualNetwork EC2 API call.
- Changes in spec and makefile.

* Thu Jul 31 2014 Mikhail Ushanov <gm.mephisto@gmail.com> - 2.4.1-12
- Added Makefile for native build in Koji
- Added support of multiple volume types
- Fix 'detach_volume' return value
- Epoch stabilized

* Thu Sep 05 2013 Nikita Kovrigin <nikitakovrigin@gmail.com> 2.9.5-3CROC 
- Added arg private_dns_name to run_instances()

* Wed Aug 07 2013 Dmitry Konishchev <konishchev@gmail.com> 2.9.5-2CROC
- Fix the epoch

* Thu Jun 13 2013 Stanislav Ievlev <stanislav.ievlev@gmail.com> 2.9.5-1
- Updated to 2.9.5

* Wed May 22 2013 Alexey I. Froloff <raorn@raorn.name> - 2.4.1-11
- Revision 2.1.1-757-gde03aa3

* Tue Dec 04 2012 Alexey I. Froloff <raorn@altlinux.org> 2.4.1-10
- Revision 2.1.1-755-gf8d9d2a

* Tue Nov 27 2012 Alexey I. Froloff <raorn@altlinux.org> 2.4.1-9
- Revision 98685889e0b138fbbc215109fb197ce6028deafb

* Tue Nov 27 2012 Alexey I. Froloff <raorn@altlinux.org> 2.4.1-8
- Revision 7d947cb5966b1c88e5b434f4260c5ca549f7e7c6

* Tue Oct  2 2012 Stanislav Ievlev <stanislav.ievlev@gmail.com> 2.4.1-7
- Revision 67676f75b9ffc13cc12e7b0ed19472d51ef4ca41

* Tue Oct  2 2012 Ruslan Bayburin <aedeph@gmail.com> 2.4.1-6
- Revision 9fcefb3a3eb4188bcc5066b5332657ce743ca9bd

* Tue Oct  2 2012 Stanislav Ievlev <stanislav.ievlev@gmail.com> 2.4.1-5
- Revision c258d896a705d67de126819b044a3a486205ae7e

* Tue Sep 11 2012 Stanislav Ievlev <stanislav.ievlev@gmail.com> 2.4.1-4
- Revision d33fb0aadf6f548916cddca2871f2dbfd960ac11

* Thu Jul 26 2012 Ruslan Bayburin <aedeph@gmail.com> 2.4.1-3
- Revision dc2c73062ff90fa902b889ce1c5aa57b2906af16

* Thu Jul 26 2012 Dmitry Konishchev <konishchev@gmail.com> 2.4.1-2
- Revision e1cf3da4298305dffc26abd04ae00a74f2fb7f12

* Fri Apr 13 2012 Stanislav Ievlev <stanislav.ievlev@gmail.com> 2.4.1-1
- Revision Next

* Wed Feb 01 2012 Dmitry Konishchev <konishchev@gmail.com> 2.1-2
- Revision 6375bb2c00160e6c73cf5ed22cb2bcf74deed7df

* Fri Aug 19 2011 Nikolay Ivanov <kolya245@gmail.com> 2.0
- Revision 71c2589e47c7b762343f4d51e22c1466478dbcec

* Sat Mar 05 2011 Dmitry Konishchev <konishchev@gmail.com> 2.0b3
- Revision d967d2b9fd4d4455e2ce4a95b0a1980a3066b5a3

