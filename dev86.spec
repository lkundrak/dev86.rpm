Summary: A real mode 80x86 assembler and linker.
Name: dev86
Version: 0.16.16
Release: 3
License: GPL
Group: Development/Languages
Source: http://www.cix.co.uk/~mayday/Dev86src-%{version}.tar.gz
Patch0: dev86-0.16.16-overflow.patch
Buildroot: %{_tmppath}/dev86/
Obsoletes: bin86
ExclusiveArch: i386

%define __os_install_post    /usr/lib/rpm/redhat/brp-compress /usr/lib/rpm/redhat/brp-strip %{__strip} /usr/lib/rpm/redhat/brp-strip-comment-note %{__strip} %{__objdump} %{nil}

%description
The dev86 package provides an assembler and linker for real mode 80x86
instructions. You'll need to have this package installed in order to
build programs that run in real mode, including LILO and the kernel's
bootstrapping code, from their sources.

You should install dev86 if you intend to build programs that run in real
mode from their source code.

%prep
%setup -q
%patch0 -p1 -b .overflow

%build
make <<EOF
5
quit
EOF

%install
rm -rf ${RPM_BUILD_ROOT}

make DIST=${RPM_BUILD_ROOT} MANDIR=%{_mandir} install install-man

# preserve READMEs
for i in bootblocks copt dis88 elksemu unproto bin86 ; do cp $i/README README.$i ; done
cp bin86/README-0.4 README-0.4.bin86
cp bin86/ChangeLog ChangeLog.bin86

cd ${RPM_BUILD_ROOT}/usr/bin
rm -f nm86 size86
ln -s objdump86 nm86
ln -s objdump86 size86

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root,-)
%doc README MAGIC Contributors README.bootblocks README.copt README.dis88
%doc README.elksemu README.unproto README-0.4.bin86 README.bin86 ChangeLog.bin86
%dir /usr/lib/bcc
/usr/bin/bcc
/usr/bin/ar86
/usr/bin/as86
/usr/bin/ld86
/usr/bin/objdump86
/usr/bin/nm86
/usr/bin/size86
/usr/bin/elksemu
/usr/lib/bcc/*
/%{_mandir}/man1/*

%changelog
* Mon Feb 14 2005 Florian La Roche <laroche@redhat.com>
- Copyright: -> License:

* Sun Dec 19 2004 Miloslav Trmac <mitr@redhat.com> - 0.16.16-2
- Fix invalid memory allocation in bcc.c:build_prefix () (#143325)

* Fri Jul 02 2004 Florian La Roche <Florian.LaRoche@redhat.de>
- 0.16.16

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 20 2004 Thomas Woerner <twoerner@redhat.com> 0.16.15-1
- new version 0.16.15

* Wed Feb 18 2004 Jeremy Katz <katzj@redhat.com> - 0.16.3-10
- rebuild

* Thu May 22 2003 Jeremy Katz <katzj@redhat.com> 0.16.3-9
- preserve README files with separate names

* Fri Jan 31 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- do not strip static archive to get rebuild working again

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Dec 12 2002 Tim Powers <timp@redhat.com> 0.16.3-6
- rebuild

* Thu Nov 14 2002 Jakub Jelinek <jakub@redhat.com>
- fix ar86 to include errno.h before using errno.

* Sat Aug 10 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- add ar86 to filelist

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jun 19 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- do not strip apps

* Mon May 27 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 0.16.3
- fix include paths
- clean up spec file

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

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

