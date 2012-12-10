%define so_version 4.17

%define	major 4
%define libname	%mklibname %{name} %{major}

Summary:	Network library, for network administrators and network hackers
Name:		lcrzo
Group:		Networking/Other
Version:	4.17.0
Release:	%mkrel 14
License:	LGPL
URL:		http://www.laurentconstantin.com/en/lcrzo/
Source0:	%{name}-%{version}-src.tar.bz2
Patch0:		lcrzo-4.17.0-genemake.patch
BuildRequires:	libpcap-devel >= 0.7.2
Provides:	liblcrzo
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Lcrzo is a network library, for network administrators and network
hackers. Its objective is to easily create network programs. This library
provides network functionnalities for Ethernet, IP, UDP, TCP, ICMP, ARP
and RARP protocols. It supports spoofing, sniffing, client and server
creation. Furthermore, lcrzo contains high level functions dealing with
data storage and handling. Using all these functions, you can quickly
create a network test program.

%package -n	%{libname}
Summary:	Shared libraries for %{name}
Group:          System/Libraries

%description -n	%{libname}
Lcrzo is a network library, for network administrators and network
hackers. Its objective is to easily create network programs. This library
provides network functionnalities for Ethernet, IP, UDP, TCP, ICMP, ARP
and RARP protocols. It supports spoofing, sniffing, client and server
creation. Furthermore, lcrzo contains high level functions dealing with
data storage and handling. Using all these functions, you can quickly
create a network test program.

%package -n	%{libname}-devel
Summary:	Development library and header files for the %{name} library
Group:		Development/Other
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel lib%{name}-devel
Obsoletes:	%{name}-devel lib%{name}-devel

%description -n	%{libname}-devel
Lcrzo is a network library, for network administrators and network
hackers. Its objective is to easily create network programs. This library 
provides network functionnalities for Ethernet, IP, UDP, TCP, ICMP, ARP 
and RARP protocols. It supports spoofing, sniffing, client and server
creation. Furthermore, lcrzo contains high level functions dealing with
data storage and handling. Using all these functions, you can quickly
create a network test program.

%prep

%setup -q -n %{name}-%{version}-src
%patch0 -p0

%build

pushd src
    ./genemake
    %make GCCOPT="%{optflags} -Wall -ansi -fPIC" \
    GCCOPTL="%{optflags} -Wall -ansi -fPIC" \
    GCCOPTP="%{optflags} -Wall -ansi -fPIC" \
    liblcrzo.a

    #make a shared lib the hard way...
    rm -f lib%{name}*.so*
    gcc -Wl,-soname,lib%{name}.so.%{major} -shared -Wl,--as-needed -Wl,--no-undefined \
    %{optflags} -fPIC -o lib%{name}%{major}.so.%{so_version} *.o -L%{_libdir} -lpcap

popd

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_mandir}/man3
install -d %{buildroot}%{_includedir}

install -m0755 src/lcrzo-config %{buildroot}%{_bindir}/lcrzo-config

# install the shared lib
install -m0755 src/lib%{name}%{major}.so.%{so_version} %{buildroot}%{_libdir}/
ln -snf lib%{name}%{major}.so.%{so_version} %{buildroot}%{_libdir}/lib%{name}%{major}.so
ln -snf lib%{name}%{major}.so.%{so_version} %{buildroot}%{_libdir}/lib%{name}.so

# install the static lib
install -m0755 src/liblcrzo.a %{buildroot}%{_libdir}/liblcrzo.a

# install headers
install -m0644 src/lcrzo*.h %{buildroot}%{_includedir}/

# install only english man pages
install -m0644 doc/man/*en.* %{buildroot}%{_mandir}/man3/

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root)
%doc README_EN.TXT
%attr(0755,root,root) %{_libdir}/lib%{name}*.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%doc doc/*en.txt doc/changelog.txt doc/credits.txt doc/todo.txt INSTALLUNIX_EN.TXT
%attr(0755,root,root) %{_bindir}/lcrzo-config
%attr(0644,root,root) %{_libdir}/*.a
%attr(0755,root,root) %{_libdir}/*.so
%attr(0644,root,root) %{_includedir}/*
%attr(0644,root,root) %{_mandir}/man3/*


%changelog
* Fri Dec 10 2010 Oden Eriksson <oeriksson@mandriva.com> 4.17.0-14mdv2011.0
+ Revision: 620058
- the mass rebuild of 2010.0 packages

* Fri Sep 11 2009 Thierry Vignaud <tv@mandriva.org> 4.17.0-13mdv2010.0
+ Revision: 438241
- rebuild

* Wed Oct 29 2008 Oden Eriksson <oeriksson@mandriva.com> 4.17.0-12mdv2009.1
+ Revision: 298272
- rebuilt against libpcap-1.0.0

* Sat Jul 19 2008 Oden Eriksson <oeriksson@mandriva.com> 4.17.0-11mdv2009.0
+ Revision: 238723
- use -Wl,--as-needed -Wl,--no-undefined

* Wed Jul 09 2008 Oden Eriksson <oeriksson@mandriva.com> 4.17.0-10mdv2009.0
+ Revision: 232977
- rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Mon Feb 18 2008 Thierry Vignaud <tv@mandriva.org> 4.17.0-9mdv2008.1
+ Revision: 170939
- rebuild
- fix "foobar is blabla" summary (=> "blabla") so that it looks nice in rpmdrake

* Fri Dec 21 2007 Olivier Blin <oblin@mandriva.com> 4.17.0-8mdv2008.1
+ Revision: 136535
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request


* Fri Feb 02 2007 Oden Eriksson <oeriksson@mandriva.com> 4.17.0-8mdv2007.0
+ Revision: 115926
- use the mkrel macro
- Import lcrzo

* Sun Jan 08 2006 Oden Eriksson <oeriksson@mandriva.com> 4.17.0-7mdk
- rebuild

* Fri Dec 31 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.17.0-6mdk
- revert latest "lib64 fixes"

* Tue Dec 28 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.17.0-5mdk
- lib64 fixes

* Sun Dec 12 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.17.0-4mdk
- fix deps

* Thu May 06 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.17.0-3mdk
- merge static-devel into the devel package
- misc spec file fixes

