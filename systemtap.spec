Summary:	Infrastructure to gather information about the running Linux system
Name:		systemtap
Epoch:		1
Version:	2.1
Release:	1
License:	GPLv2+
Group:		Development/Kernel
URL:		http://sourceware.org/systemtap/
Source0:	http://sourceware.org/systemtap/ftp/releases/%{name}-%{version}.tar.gz
Patch2:		systemtap-2.0-rpmlib.h.patch
Buildrequires:	elfutils-static-devel
BuildRequires:	gtkmm2.4-devel
BuildRequires:	libavahi-client-devel
BuildRequires:	latex2html
BuildRequires:	pkgconfig(libglade-2.0)
BuildRequires:	nss-devel
BuildRequires:	nspr-devel
BuildRequires:	rpm-devel
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
%apply_patches

%build
#fix build with new automake
sed -i -e 's,AM_PROG_CC_STDC,AC_PROG_CC,g' configure.*
autoreconf -fi
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
