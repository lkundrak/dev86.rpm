Summary: A real mode 80x86 assembler and linker.
Name: dev86
Version: 0.15.5
Release: 1
Copyright: GPL
Group: Development/Languages
Source: http://www.cix.co.uk/~mayday/Dev86src-%{version}.tar.gz
Patch0: Dev86src-0.15.5-noroot.patch
Patch1: Dev86src-0.14-nobcc.patch
Patch2: Dev86src-0.15-bccpaths.patch
Patch3: Dev86src-0.15-mandir.patch
Patch4: Dev86src-0.15.5-badlinks.patch
Buildroot: %{_tmppath}/dev86/
Obsoletes: bin86
ExclusiveArch: i386

%description
The dev86 package provides an assembler and linker for real mode 80x86
instructions. You'll need to have this package installed in order to
build programs that run in real mode, including LILO and the kernel's
bootstrapping code, from their sources.

You should install dev86 if you intend to build programs that run in real
mode from their source code.

%prep
%setup -q -n linux-86
%patch0 -b .oot -p1
%patch1 -b .djb -p1
%patch2 -b .bccpaths -p1
%patch3 -b .mandir -p1
%patch4 -b .fix -p1

%build
make <<!FooBar!
5
quit
!FooBar!

%install
rm -rf ${RPM_BUILD_ROOT}

make DIST=${RPM_BUILD_ROOT} MANDIR=${RPM_BUILD_ROOT}/%{_mandir} install

install -m 755 -s ${RPM_BUILD_ROOT}/lib/elksemu ${RPM_BUILD_ROOT}/usr/bin
rm -rf ${RPM_BUILD_ROOT}/lib/

cd ${RPM_BUILD_ROOT}/usr/bin
rm -f nm86 size86
ln -s objdump86 nm86
ln -s objdump86 size86

#strip ${RPM_BUILD_ROOT}/usr/bin/as86
#strip ${RPM_BUILD_ROOT}/usr/bin/bcc
#strip ${RPM_BUILD_ROOT}/usr/bin/ld86
#strip ${RPM_BUILD_ROOT}/usr/bin/objdump86
#strip ${RPM_BUILD_ROOT}/usr/lib/bcc/bcc-cc1
#strip ${RPM_BUILD_ROOT}/usr/lib/bcc/copt
#strip ${RPM_BUILD_ROOT}/usr/lib/bcc/unproto

# move header files out of /usr/include and into /usr/lib/bcc/include
mv ${RPM_BUILD_ROOT}/usr/include ${RPM_BUILD_ROOT}/usr/lib/bcc

%clean
#rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root,-)
%doc README MAGIC Contributors bootblocks/README copt/README dis88/README
%doc elksemu/README unproto/README bin86/README-0.4 bin86/README bin86/ChangeLog
%dir /usr/lib/bcc
%dir /usr/lib/bcc/i86
%dir /usr/lib/bcc/i386
%dir /usr/lib/bcc/include
/usr/bin/bcc
/usr/bin/as86
/usr/bin/as86_encap
/usr/bin/ld86
/usr/bin/objdump86
/usr/bin/nm86
/usr/bin/size86
/usr/lib/bcc/bcc-cc1
/usr/lib/bcc/copt
/usr/lib/bcc/unproto
/usr/lib/bcc/i86/*
/usr/lib/bcc/i386/*
/usr/lib/liberror.txt
/usr/lib/bcc/include/*
/usr/bin/elksemu
/%{_mandir}/man1/*

%changelog
* Mon May  7 2001 Bernhard Rosenkraenzer <bero@redhat.com> 0.15.5-1
- Update to 0.15.5, lots of fixes

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Mon Jun 19 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- add defattr

* Sun Jun 18 2000 Matt Wilson <msw@redhat.com>
- use %%{_mandir}

* Fri Feb 04 2000 Nalin Dahyabhai <nalin@redhat.com>
- change default header directory to match libs and fix bug #9121

* Thu Feb 03 2000 Cristian Gafton <gafton@redhat.com>
- version 0.15.0
- man pages are compressed

* Mon Sep 20 1999 Donnie Barnes <djb@redhat.com>
- removed "Distribution:" line (was RHCN)
- changed description and summary to the ones from bin86 with s/bin/dev/
  done throughout
- added patch to keep from installing in /usr/bcc and simply in /usr
- moved include files to /usr/lib/bcc/include

* Tue Sep 07 1999 Erik Troan <ewt@redhat.com>
- updated to Dev86src
- included in Red Hat 6.1

* Sat Nov 14 1998 Simon Weijgers <simon@mbit.doa.org>

- First release of this package to be shipped to rhcn.

- To be fixed: Bug in Makefile which installs headerfiles
  double. E.g. /usr/bcc/include/arch is also installed under
  /usr/bcc/include/arch/arch. This doesn't hinder operation,
  just eats a tiny bit of diskspace.

