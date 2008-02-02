%define name    kerneloops
%define version 0.10
%define release %mkrel 1

Name:           %{name}
Version:        %{version}
Release:        %{release}
Summary:        Tool to automatically collect and submit kernel crash signatures

Group:          System/Kernel and hardware
License:        GPLv2
URL:            http://www.kerneloops.org
Source0:        http://www.kerneloops.org/download/%{name}-%{version}.tar.gz
Patch0:         kerneloops-0.10-fix-manfile-name.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}

BuildRequires:  curl-devel
BuildRequires:  libnotify-devel
BuildRequires:  gtk2-devel
BuildRequires:  dbus-glib-devel
BuildRequires:  gettext
BuildRequires:  desktop-file-utils
Requires(post): rpm-helper
Requires(preun): rpm-helper

%description
This package contains the tools to collect kernel crash signatures,
and to submit them to the kerneloops.org website where the kernel
crash signatures get collected and grouped for presentation to the
Linux kernel developers.

%prep
%setup -q
%patch0 -p1

%build
%make

%check
make tests

%install
%makeinstall_std
mkdir -m 0755 -p %{buildroot}%{_initrddir}
install -p -m 0755 kerneloops.init %{buildroot}%{_initrddir}/%{name}
%find_lang %{name}

%post 
%_post_service kerneloops

%preun
%_preun_service kerneloops

%files -f %{name}.lang
%defattr(-,root,root)
%doc Changelog
%{_sbindir}/%{name}
%config(noreplace) %{_sysconfdir}/kerneloops.conf
%{_initrddir}/%{name}
%{_sysconfdir}/dbus-1/system.d/kerneloops.dbus
%{_sysconfdir}/xdg/autostart/kerneloops-applet.desktop
%{_datadir}/kerneloops/
%{_bindir}/kerneloops-applet
%doc %{_mandir}/man8/kerneloops.8.*
