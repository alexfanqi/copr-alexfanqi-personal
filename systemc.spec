Name:           systemc
Version:        3.0.0
Release:        1%{?dist}
Summary:        SystemC is a set of C++ classes and macros which provide an event-driven simulation interface

License:        ASL 2.0 
URL:            https://www.accellera.org/downloads/standards/systemc
Source0:        https://github.com/accellera-official/systemc/archive/refs/tags/3.0.0.tar.gz

Patch0: https://github.com/alexfanqi/copr-alexfanqi-personal/raw/master/systemc-CMakeLists-build-both-static-and-dynamic.patch
Patch1: https://github.com/alexfanqi/copr-alexfanqi-personal/raw/master/systemc-install-pkgconf.patch

BuildRequires:  cmake ninja-build chrpath cmake binutils gcc gcc-c++

%description
SystemC addresses the need for a system design and verification language that spans hardware 
and software. It is a language built in standard C++ by extending the language with a set of class libraries 
created for design and verification. Users worldwide are applying SystemC to system-level modeling, abstract 
analog/mixed-signal modeling, architectural exploration, performance modeling, software development, 
functional verification, and high-level synthesis.

%package devel
Summary:        systemc-devel contains SystemC headers and a statically linkable library.

%description devel
SystemC addresses the need for a system design and verification language that spans hardware 
and software. It is a language built in standard C++ by extending the language with a set of class libraries 
created for design and verification. Users worldwide are applying SystemC to system-level modeling, abstract 
analog/mixed-signal modeling, architectural exploration, performance modeling, software development, 
functional verification, and high-level synthesis.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%define __builder ninja
%cmake -DCMAKE_INSTALL_PREFIX=%{_prefix} -DCMAKE_INSTALL_INCLUDEDIR=include/systemc -DCMAKE_BUILD_TYPE=Release -DCMAKE_CXX_STANDARD=17 -G Ninja .
%cmake_build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p %{buildroot}%{_bindir}
%cmake_install
chrpath --delete %{buildroot}%{_libdir}/libsystemc.so.%{version}

%files
%license %{_datadir}/doc/systemc/LICENSE
%doc %{_datadir}/doc/systemc
%{_libdir}/libsystemc.so*

%files devel
%{_libdir}/libsystemc.a
%{_libdir}/cmake
%{_includedir}/systemc
%{_datadir}/pkgconfig/*.pc

%changelog
* Tue May 18 2021 Roy Spliet <nouveau@spliet.org>
- Rebase to SystemC 3.0

* Tue May 18 2021 Roy Spliet <nouveau@spliet.org>
- Update specfile to fix build for F33/F34

* Fri Jun  7 2019 Roy Spliet <nouveau@spliet.org>
- Initial release

