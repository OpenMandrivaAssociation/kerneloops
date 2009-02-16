Summary:	Tool to automatically collect and submit kernel crash signatures
Name:		kerneloops
Version:	0.12
Release:	%mkrel 2
Group:		System/Kernel and hardware
License:	GPLv2
URL:		http://www.kerneloops.org
Source0:	http://www.kerneloops.org/download/%{name}-%{version}.tar.gz
Source1:	kerneloops.service
# (tpg) https://bugzilla.redhat.com/show_bug.cgi?id=479580
Patch0:		kerneloops-0.12-dbus-init.patch
Patch1:		kerneloops-0.12-format_not_a_string_literal_and_no_format_arguments.patch
Patch2:		kerneloops-0.12-makefile.patch
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
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%make CFLAGS="%{optflags}" LDFLAGS="%{ldflags}"

%check
make tests

%install
rm -rf %{buildroot}
%makeinstall_std

mkdir -p %{buildroot}%{_datadir}/dbus-1/system-services
install -m 644 %{SOURCE1} %{buildroot}%{_datadir}/dbus-1/system-services/org.kerneloops.submit.service

%find_lang %{name}

%triggerun -- kerneloops < 0.12-2
/sbin/chkconfig --del kerneloops

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%doc Changelog
%config(noreplace) %{_sysconfdir}/kerneloops.conf
%{_sbindir}/%{name}
%{_bindir}/kerneloops-applet
%{_datadir}/kerneloops
%{_datadir}/dbus-1/system-services/*.service
%{_sysconfdir}/dbus-1/system.d/kerneloops.dbus
%{_sysconfdir}/xdg/autostart/kerneloops-applet.desktop
%{_mandir}/man8/kerneloops.8.*
