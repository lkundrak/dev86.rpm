Summary: A real mode 80x86 assembler and linker
Name: dev86
Version: 0.16.17
Release: 14%{?dist}
License: GPL+ and GPLv2+ and LGPLv2+
Group: Development/Languages
URL: http://homepage.ntlworld.com/robert.debath/
Source: http://homepage.ntlworld.com/robert.debath/dev86/Dev86src-%{version}.tar.gz
Patch0: dev86-noelks.patch
Patch1: dev86-64bit.patch
Patch2: dev86-nostrip.patch
Patch3: dev86-overflow.patch
Patch4: dev86-long.patch
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Obsoletes: bin86

# don't try to strip binaries generated by dev86 unknown to /usr/bin/strip
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
%patch0 -p1 -b .noelks
%if %{__isa_bits} == 64
%patch1 -p1 -b .64bit
%endif
%patch2 -p1 -b .nostrip
%patch3 -p1 -b .overflow
%patch4 -p1 -b .long

%build
# the main makefile doesn't allow parallel build
make bcc86 unproto copt as86 ld86 CFLAGS="$RPM_OPT_FLAGS"
make -C cpp CFLAGS="$RPM_OPT_FLAGS" %{?_smp_mflags}
make -C ar CFLAGS="$RPM_OPT_FLAGS" %{?_smp_mflags}
make -C ld CFLAGS="$RPM_OPT_FLAGS" %{?_smp_mflags}
# ncc doesn't support gcc optflags
make

%install
rm -rf ${RPM_BUILD_ROOT}

make	DIST=${RPM_BUILD_ROOT} \
	MANDIR=%{_mandir} \
	LIBDIR=%{_libdir}/bcc \
	INCLDIR=%{_libdir}/bcc \
	LOCALPREFIX=%{_prefix} \
	install install-man

# preserve READMEs
for i in bootblocks copt dis88 unproto bin86 ; do cp $i/README README.$i ; done
cp bin86/README-0.4 README-0.4.bin86
cp bin86/ChangeLog ChangeLog.bin86
mv libc/COPYING COPYING.LGPL

pushd ${RPM_BUILD_ROOT}%{_bindir}
rm -f nm86 size86
ln -s objdump86 nm86
ln -s objdump86 size86
popd

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root,-)
%doc README MAGIC Contributors README.bootblocks README.copt README.dis88
%doc README.unproto README-0.4.bin86 README.bin86 ChangeLog.bin86 COPYING
%doc COPYING.LGPL
%dir %{_libdir}/bcc
%{_bindir}/bcc
%{_bindir}/ar86
%{_bindir}/as86
%{_bindir}/ld86
%{_bindir}/objdump86
%{_bindir}/nm86
%{_bindir}/size86
%{_libdir}/bcc/*
%{_mandir}/man1/*

%changelog
* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16.17-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 19 2009 Jindrich Novy <jnovy@redhat.com> 0.16.17-13
- fix buffer overflow caused by realpath() call
- attempt to fix type width size for 64bit arches
- merge review fixes (#225683):
  - remove BR: gawk
  - add licenses to documentation
  - use RPM_OPT_FLAGS to compile arch dependent binaries

* Tue Feb 17 2009 Jindrich Novy <jnovy@redhat.com> 0.16.17-12
- apply 64bit fix to all platforms, not only on x86_64,
  thanks to Glauber Costa

* Mon Feb 16 2009 Jindrich Novy <jnovy@redhat.com> 0.16.17-11
- remove ExclusiveArch to allow to run dev86 on different arches

* Wed Jul 16 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.16.17-10
- fix license tag

* Mon Feb 25 2008 Jindrich Novy <jnovy@redhat.com> 0.16.17-9
- manual rebuild because of gcc-4.3 (#434186)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.16.17-8
- Autorebuild for GCC 4.3

* Mon Sep 17 2007 Jindrich Novy <jnovy@redhat.com> - 0.16.17-7
- don't ifarch patch definition

* Thu Aug 27 2007 Jindrich Novy <jnovy@redhat.com> - 0.16.17-6
- add missing BR on gawk
- rebuild (#249952)

* Tue Jan 30 2007 Jindrich Novy <jnovy@redhat.com> - 0.16.17-5
- don't strip debuginfo

* Wed Dec 27 2006 Jindrich Novy <jnovy@redhat.com> - 0.16.17-4
- bcc now searches in correct path for bcc-cpp on x86_64 (#219697)

* Tue Dec  5 2006 Jindrich Novy <jnovy@redhat.com> - 0.16.17-3
- make the dev86 spec less tragic -> use macros, don't conflict
  on multiarches, add URL, fix BuildRoot, fix rpmlint warnings

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.16.17-2.2
- rebuild

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.16.17-2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Jan 25 2006 Jeremy Katz <katzj@redhat.com> - 0.16.17-2
- build on x86_64
- don't build elks (it's not happy on x86_64)

* Wed Mar 02 2005 Karsten Hopp <karsten@redhat.de> 0.16.17-1 
- update and rebuild with gcc-4
- drop obsolete overflow patch

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

