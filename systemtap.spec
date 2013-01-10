Summary:	Infrastructure to gather information about the running Linux system
Name:		systemtap
Epoch:		1
Version:	2.0
Release:	1
License:	GPLv2+
Group:		Development/Kernel
URL:		http://sourceware.org/systemtap/
Source0:	http://sourceware.org/systemtap/ftp/releases/%{name}-%{version}.tar.gz
Buildrequires:	elfutils-static-devel
BuildRequires:	gtkmm2.4-devel
Buildrequires:	libavahi-client-devel
Buildrequires:	latex2html
BuildRequires:	libglade2.0-devel
BuildRequires:	nss-devel
BuildRequires:	nspr-devel
BuildRequires:	rpm-devel
BuildRequires:	pkgconfig
BuildRequires:	gettext
BuildRequires:	gettext-devel
BuildRequires:	xmlto
BuildRequires:	texlive
BuildRequires:	libcap-devel

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


%prep
%setup -q
#patch0 -p1 -b .rpm5~
#patch1 -p1 -b .automake~

%build
sed -i \
        -e 's:-Werror::g' \
        configure.ac Makefile.am \
        grapher/Makefile.am \
        runtime/staprun/Makefile.am \
        buildrun.cxx \
        runtime/bench2/bench.rb \
        runtime/bench2/Makefile \
        testsuite/systemtap.unprivileged/unprivileged_probes.exp \
        testsuite/systemtap.unprivileged/unprivileged_myproc.exp \
        testsuite/systemtap.base/stmt_rel_user.exp \
        testsuite/systemtap.base/sdt_va_args.exp \
        testsuite/systemtap.base/sdt_misc.exp \
        testsuite/systemtap.base/sdt.exp \
        scripts/kprobes_test/gen_code.py

# (tpg) for new automake
#sed -i -e 's/AM_PROG_CC_STDC/AC_PROG_CC/g' configure.ac

#autoreconf -fi
%configure2_5x	\
	--with-rpm \
	--disable-rpath

%make

%install
%makeinstall

# we add testsuite with a lot of examples
install -m 766 -d testsuite %{buildroot}/%{_datadir}/%{name}/

%files
%doc AUTHORS INSTALL HACKING README
%{_bindir}/dtrace
%{_bindir}/stap*
%{_mandir}/man*/*
%{_libdir}/%{name}/*
%{_datadir}/%{name}/*
%{_includedir}/sys/sdt.h
%{_includedir}/sys/sdt-config.h
%{_localedir}/*/LC_MESSAGES/systemtap.mo
