Summary: 	Infrastructure to gather information about the running Linux system
Name: 		systemtap
Epoch:		1
Version: 	1.3
Release: 	%mkrel 2
License: 	GPLv2+
Group: 		Development/Kernel
URL: 		http://sourceware.org/systemtap/
Source: 	http://sourceware.org/systemtap/ftp/releases/systemtap-%{version}.tar.gz
BuildRoot: 	%{_tmppath}/%{name}-%{version}-%{release}-root
Buildrequires:	libcap-devel
Buildrequires:	elfutils-static-devel
BuildRequires:	gtkmm2.4-devel
Buildrequires:	libavahi-client-devel
Buildrequires:	latex2html
BuildRequires:	libglade2.0-devel


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

%build
%configure2_5x
%make


%install
rm -rf $RPM_BUILD_ROOT
# cd src
%makeinstall

# we add testsuite with a lot of examples
install -m 766 -d testsuite $RPM_BUILD_ROOT/%{_datadir}/%{name}/


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc AUTHORS INSTALL HACKING README
%{_bindir}/dtrace
%{_bindir}/stap*
%{_mandir}/man*/*
%{_libdir}/%{name}/*
%{_datadir}/%{name}/*
%{_includedir}/sys/sdt.h
