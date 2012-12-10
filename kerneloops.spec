Summary:	Tool to automatically collect and submit kernel crash signatures
Name:		kerneloops
Version:	0.12
Release:	%mkrel 8
Group:		System/Kernel and hardware
License:	GPLv2
URL:		http://www.kerneloops.org
Source0:	http://www.kerneloops.org/download/%{name}-%{version}.tar.gz
###bor###Source1:	kerneloops.service
# (tpg) https://bugzilla.redhat.com/show_bug.cgi?id=479580
###bor###Patch0:		kerneloops-0.12-dbus-init.patch
Patch1:		kerneloops-0.12-format_not_a_string_literal_and_no_format_arguments.patch
Patch2:		kerneloops-0.12-makefile.patch
Patch3:		kerneloops-0.12-libnotify.patch
BuildRequires:	curl-devel
BuildRequires:	libnotify-devel
BuildRequires:	gtk2-devel
BuildRequires:	dbus-glib-devel
BuildRequires:	gettext
BuildRequires:	desktop-file-utils
Requires(post):	rpm-helper
Requires(preun):	rpm-helper
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
This package contains the tools to collect kernel crash signatures,
and to submit them to the kerneloops.org website where the kernel
crash signatures get collected and grouped for presentation to the
Linux kernel developers.

%prep
%setup -q
###bor###%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p0

%build
%if %mdkver >= 201200
%serverbuild_hardened
%else
%serverbuild
%endif

%make CFLAGS="%{optflags}" LDFLAGS="%{ldflags}"

rm -rf %{buildroot}
%makeinstall_std
mkdir -m 0755 -p %{buildroot}%{_initrddir}
install -p -m 0755 kerneloops.init %{buildroot}%{_initrddir}/%{name}

###bor###mkdir -p %{buildroot}%{_datadir}/dbus-1/system-services
###bor###install -m 644 %{SOURCE1} %{buildroot}%{_datadir}/dbus-1/system-services/org.kerneloops.submit.service

%find_lang %{name}

%post
%_post_service kerneloops

###bor###%triggerun -- kerneloops < 0.12-2
###bor###/sbin/chkconfig --del kerneloops

# Updating from 0.12-2 won't add service thinking it is upgrade.
# Force add service by simulating initial install
%triggerun -- kerneloops == 0.12-2mdv2009.1
%_add_service_helper %{name} 1 %{name}

%preun
%_preun_service kerneloops
%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%doc Changelog
%config(noreplace) %{_sysconfdir}/kerneloops.conf
%{_initrddir}/%{name}
%{_sbindir}/%{name}
%{_bindir}/kerneloops-applet
%{_datadir}/kerneloops
###bor###%{_datadir}/dbus-1/system-services/*.service
%{_sysconfdir}/dbus-1/system.d/kerneloops.dbus
%{_sysconfdir}/xdg/autostart/kerneloops-applet.desktop
%{_mandir}/man8/kerneloops.8.*


%changelog
* Tue Oct 11 2011 Tomasz Pawel Gajc <tpg@mandriva.org> 0.12-8mdv2012.0
+ Revision: 704377
- use %%serverbuild_hardened macro for mdv2012

* Sat Apr 30 2011 Funda Wang <fwang@mandriva.org> 0.12-7
+ Revision: 661051
- fix link with libnotify and dbus

* Fri Dec 10 2010 Oden Eriksson <oeriksson@mandriva.com> 0.12-6mdv2011.0
+ Revision: 619958
- the mass rebuild of 2010.0 packages

* Thu Oct 08 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 0.12-5mdv2010.0
+ Revision: 455872
- rebuild for new curl SSL backend

* Fri Sep 11 2009 Thierry Vignaud <tv@mandriva.org> 0.12-4mdv2010.0
+ Revision: 438090
- rebuild

* Sun Mar 29 2009 Andrey Borzenkov <arvidjaar@mandriva.org> 0.12-3mdv2009.1
+ Revision: 362158
- Revert to starting service via initscript. Kerneloops does not register
  service name with D-Bus, so every kerneloops-applet launch (on login)
  spawned new kerneloops daemon.

* Mon Feb 16 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 0.12-2mdv2009.1
+ Revision: 341048
- Patch0: start kerneloops via d-bus
- Patch1: fix building with -Werror=format-string
- Patch2: compile with %%ldflags
- compile with %%optflags
- spec file clean

* Fri Oct 10 2008 Frederik Himpe <fhimpe@mandriva.org> 0.12-1mdv2009.1
+ Revision: 291656
- update to new version 0.12

* Fri Aug 08 2008 Thierry Vignaud <tv@mandriva.org> 0.11-2mdv2009.0
+ Revision: 267783
- rebuild early 2009.0 package (before pixel changes)

* Tue Apr 29 2008 Frederik Himpe <fhimpe@mandriva.org> 0.11-1mdv2009.0
+ Revision: 199046
- New upstream version: remove patch0 integrated upstream

* Sat Feb 02 2008 Frederik Himpe <fhimpe@mandriva.org> 0.10-1mdv2008.1
+ Revision: 161517
- import kerneloops

