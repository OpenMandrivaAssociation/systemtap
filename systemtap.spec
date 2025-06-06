%ifarch %{riscv}
# FIXME The RISC-V port doesn't have java yet, but
# we can crosscompile
%if %{cross_compiling}
%bcond_without	java
%else
%bcond_with	java
%endif
%else
%bcond_without	java
%endif
%define _disable_ld_no_undefined %nil

%bcond_without	avahi
%bcond_without	docs

Summary:	Infrastructure to gather information about the running Linux system
Name:		systemtap
Version:	5.3
Release:	1
License:	GPLv2+
Group:		Development/Kernel
Url:		https://sourceware.org/systemtap/
Source0:	http://sourceware.org/systemtap/ftp/releases/%{name}-%{version}.tar.gz
#Patch0:		systemtap-4.7-python-3.11.patch
Patch3:		systemtap-2.5-fix-aliasing-violations.patch

BuildRequires:	cap-devel
BuildRequires:	elfutils-devel
BuildRequires:	gettext
BuildRequires:	gettext-devel
BuildRequires:	pkgconfig(libvirt)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(json-c)
BuildRequires:	pkgconfig(ncursesw)
BuildRequires:	boost-devel
#BuildRequires:	latex2html
%if %{with avahi}
BuildRequires:	pkgconfig(avahi-client)
%endif
%if %{with docs}
BuildRequires:	xmlto
BuildRequires:	texlive-dvips texlive-charter texlive-mathdesign
%endif
BuildRequires:	pkgconfig(nss)
BuildRequires:	pkgconfig(nspr)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(python3)
BuildRequires:	python-setuptools
BuildRequires:	pkgconfig(rpm)
BuildRequires:	pkgconfig(popt)
%if %{with java}
BuildRequires:	jpackage-utils jdk-current
%endif

Provides:	/usr/bin/stap

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

%description	runtime
SystemTap is an instrumentation system for systems running Linux.
This package contains the runtime environment for systemtap programs.

%package	examples
Summary:	Examples for systemtap
Group:		Development/Other

%description	examples
SystemTap is an instrumentation system for systems running Linux.
This package contains examples for systemtap programs.

%if %{with java}
%package	runtime-java
Summary:	Systemtap Java Runtime Support
Group:		Development/Java
Requires:	systemtap-runtime = %{EVRD}
# Not packaged yet..
#Requires:	byteman > 2.0

%description	runtime-java
This package includes support files needed to run systemtap scripts
that probe Java processes running on the OpenJDK 1.6 and OpenJDK 1.7
runtimes using Byteman.
%endif

%package	server
Summary:	Systemtap server
Group:		Development/Other
Requires:	%{name} = %{EVRD}

%description	server
SystemTap is an instrumentation system for systems running Linux.
This package contains the server component of systemtap.

%package	exporter
Summary:	Systemtap-prometheus interoperation mechanism
Group:		Development/Kernel
License:	GPLv2+
URL:		https://sourceware.org/systemtap/

%description exporter
This package includes files for a systemd service that manages
systemtap sessions and relays prometheus metrics from the sessions
to remote requesters on demand.

%package	devel
Summary:	Header files for %{name}
Group:		Development/Other
Requires:	%{name} = %{EVRD}

%description	devel
The package includes the header files for %{name}.

%prep
%autosetup -p1

sed -i 's!$(DESTDIR)$(prefix)/lib/systemd!$(DESTDIR)/lib/systemd!g' stap-exporter/Makefile.*

autoreconf -fi

%build
%if %{with java}
. %{_sysconfdir}/profile.d/90java.sh
%endif

%global optflags %{optflags} -Wno-error
# FIXME at the moment disabling avahi also disables nss and libvirt
# That's because all 3 are disabled for bootstrapping. Might make sense
# to have separate options for more customization options.
%configure	--with-rpm \
		--without-python2-probes \
		--without-selinux \
		--with-python3 \
%if %{with java}
		--with-java=/usr/lib/jvm/java \
%else
		--without-java \
%endif
%if %{without avahi}
		--without-avahi \
		--without-nss \
		--disable-libvirt \
%endif
		--enable-sqlite \
		--disable-docs
%make_build

%install
%make_install

# we add testsuite with a lot of examples
install -m 766 -d testsuite %{buildroot}%{_datadir}/%{name}/

%find_lang %{name} --with-man

%files
%{_bindir}/stap
%{_bindir}/stap-prep
%{_bindir}/stap-jupyter-container
%{_bindir}/stap-jupyter-install
%if ! %{without avahi}
%{_bindir}/stapvirt
%endif
/lib/systemd/system/stap-exporter.service
%{_bindir}/stap-profile-annotate
%{_mandir}/man[17]/*
%lang(cs) %{_mandir}/cs/man[17]/*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/tapset

%files examples
%{_datadir}/%{name}/examples

%files runtime -f systemtap.lang
%{_bindir}/stapbpf
%{_bindir}/staprun
%{_bindir}/stapsh
%{_bindir}/stap-merge
%{_bindir}/stap-report
%{_datadir}/%{name}
%dir %{_libexecdir}/%{name}
%{_libexecdir}/%{name}/stapio
%{_libexecdir}/%{name}/stap-env
%if ! %{without avahi}
%{_libexecdir}/%{name}/stap-authorize-cert
%endif
%{_libexecdir}/%{name}/python
%{_libdir}/python3*/site-packages/HelperSDT*
%{_mandir}/man8/stapbpf.8.*
%{_mandir}/man8/staprun.8*
%{_mandir}/man8/stapsh.8.*
%{_mandir}/man8/systemtap-service.8.*
%lang(cs) %{_mandir}/cs/man8/stapsh.8*

%if %{with java}
%files runtime-java
%dir %{_libexecdir}/systemtap
%{_libexecdir}/systemtap/libHelperSDT.so
%{_libexecdir}/systemtap/HelperSDT.jar
%{_libexecdir}/systemtap/stapbm
%endif

%if ! %{without avahi}
%files server
%{_bindir}/stap-server
%{_libexecdir}/%{name}/stap-gen-cert
%{_libexecdir}/%{name}/stap-serverd
%{_libexecdir}/%{name}/stap-sign-module
%{_libexecdir}/%{name}/stap-start-server
%{_libexecdir}/%{name}/stap-stop-server
%{_mandir}/man8/stap-server.8*
%lang(cs) %{_mandir}/cs/man8/stap-server.8*
%endif

%files exporter
%{_sysconfdir}/stap-exporter
%{_sysconfdir}/sysconfig/stap-exporter
%{_mandir}/man8/stap-exporter.8*
%{_sbindir}/stap-exporter

%files devel
%{_bindir}/dtrace
%{_includedir}/sys/*.h
%{_datadir}/%{name}/runtime
%{_mandir}/man3/*.3*
%lang(cs) %{_mandir}/cs/man3/*
