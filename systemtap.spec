%define name 		systemtap
%define date		20080614
%define version 	0.%{date}.1
%define release 	%mkrel 1


Summary: 	Infrastructure to gather information about the running Linux system
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
License: 	GPL
Group: 		Development/Kernel
URL: 		http://sourceware.org/systemtap/
Source0: 	%{name}-%{date}.tar.bz2
BuildRoot: 	%{_tmppath}/%{name}-%{version}-%{release}-root
Buildrequires:	libcap-devel
Buildrequires:	elfutils-static-devel
Buildrequires:	elfutils-devel


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
# %setup -q -n %{name}-%{date}
%setup -q -n src


%build
# cd src
%configure
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
%{_bindir}/stap*
%{_mandir}/man*/*
%{_libdir}/%{name}/*
%{_datadir}/%{name}/*
