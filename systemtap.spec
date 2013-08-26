Summary:	Infrastructure to gather information about the running Linux system
Name:		systemtap
Epoch:		1
Version:	2.3
Release:	2
License:	GPLv2+
Group:		Development/Kernel
Url:		http://sourceware.org/systemtap/
Source0:	http://sourceware.org/systemtap/ftp/releases/%{name}-%{version}.tar.gz
Patch2:		systemtap-2.2-rpm5.patch
Patch3:		systemtap-2.2-fix-aliasing-violations.patch
Patch4:		systemtap-2.2-automake1.3-fix.patch
Buildrequires:	elfutils-devel
BuildRequires:	pkgconfig(gtkmm-2.4)
BuildRequires:	pkgconfig(avahi-client)
BuildRequires:	latex2html
BuildRequires:	pkgconfig(libglade-2.0)
BuildRequires:	pkgconfig(nss)
BuildRequires:	pkgconfig(nspr)
BuildRequires:	gettext
BuildRequires:	gettext-devel
BuildRequires:	xmlto
BuildRequires:	texlive-dvips
BuildRequires:	cap-devel
Buildrequires:	elfutils-devel
BuildRequires:	gettext-devel
BuildRequires:	pkgconfig(avahi-client)
BuildRequires:	pkgconfig(gtkmm-2.4)
BuildRequires:	pkgconfig(libglade-2.0)
BuildRequires:	pkgconfig(nspr)
BuildRequires:	pkgconfig(nss)

%description
SystemTap provides free software (GPL) infrastructure to simplify the gathering
of information about the running Linux system. This assists diagnosis of a 
performance or functional problem. SystemTap eliminates the need for the 
developer to go through the tedious and disruptive instrument, recompile, 
install, and reboot sequence that may be otherwise required to collect data.

SystemTap provides a simple command line interface and scripting language for
writing instrumentation for a live running kernel. We are publishing samples, 
as well as enlarging the internal "tapset" script library to aid reuse and 
abstraction. We also plan to support probing userspace applications. We are 
investigating interfacing Systemtap with similar tools such as Frysk, 
Oprofile and LTT.

Current project members include Red Hat, IBM, Intel, and Hitachi.

%package	runtime
Summary:	Runtime environment for systemtap
Group:		Development/Other
Conflicts:	systemtap < 1:2.1-3

%description	runtime
SystemTap is an instrumentation system for systems running Linux.
This package contains the runtime environment for systemtap programs.

%package	server
Summary:	Systemtap server
Group:		Development/Other
Requires:	%{name} = %{EVRD}
Conflicts:	systemtap < 1:2.1-3

%description	server
SystemTap is an instrumentation system for systems running Linux.
This package contains the server component of systemtap.

%package	devel
Summary:	Header files for %{name}
Group:		Development/Other
Requires:	%{name} = %{EVRD}
Conflicts:	systemtap < 1:2.1-3

%description devel
The package includes the header files for %{name}.

%prep
%setup -q
%apply_patches
aclocal --force
autoreconf -fi

%build
%global optflags %{optflags} -Wno-error
%configure2_5x	--with-rpm \
		--without-selinux

%make

%install
%makeinstall

# we add testsuite with a lot of examples
install -m 766 -d testsuite %{buildroot}%{_datadir}/%{name}/

%find_lang %{name}

%files
%{_bindir}/stap
%{_mandir}/man[17]/*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/tapset

%files runtime -f systemtap.lang
%doc %{_docdir}/systemtap
%{_bindir}/staprun
%{_bindir}/stapsh
%{_bindir}/stap-merge
%{_bindir}/stap-report
%dir %{_libexecdir}/%{name}
%{_libexecdir}/%{name}/stapio
%{_libexecdir}/%{name}/stap-env
%{_libexecdir}/%{name}/stap-authorize-cert
%{_mandir}/man8/staprun.8*
%{_mandir}/man8/stapsh.8.*

%files server
%{_bindir}/stap-server
%{_libexecdir}/%{name}/stap-gen-cert
%{_libexecdir}/%{name}/stap-serverd
%{_libexecdir}/%{name}/stap-sign-module
%{_libexecdir}/%{name}/stap-start-server
%{_libexecdir}/%{name}/stap-stop-server
%{_mandir}/man8/stap-server.8*

%files devel
%{_bindir}/dtrace
%{_includedir}/sys/*.h
%{_datadir}/%{name}/runtime
%{_mandir}/man3/*.3*
