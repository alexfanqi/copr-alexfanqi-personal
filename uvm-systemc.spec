%global src_version 1.0-beta6

Name:           uvm-systemc
Version:        1.0beta6
Release:        %autorelease
Summary:        Universal Verification Methodology (UVM) for SystemC

License:        Apache-2.0
URL:            https://systemc.org/overview/uvm-systemc-faq/
Source0:        https://www.accellera.org/images/downloads/drafts-review/%{name}-%{src_version}.tar.gz
BuildRequires:  systemc-devel >= 2.3
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
Requires:       systemc >= 2.3

%description
The Universal Verification Methodology (UVM) is a standard for verifying integrated circuit designs. 
This package provides the UVM library for SystemC, enabling advanced verification techniques 
in a SystemC-based environment.

%package devel
Summary:        Development files for uvm-systemc
Requires:       uvm-systemc = %{version}-%{release}

%description devel
Development files for uvm-systemc

%prep
%setup -q -n %{name}-%{src_version}

%build
./configure --prefix=%{_prefix} --libdir=%{_libdir} --includedir=%{_includedir}/uvm-systemc --with-arch-suffix=no --with-systemc=%{_prefix}
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

%files
%license %{_prefix}/LICENSE
%doc %{_prefix}/docs/*.pdf
%doc %{_prefix}/NOTICE
%doc %{_prefix}/README.md
%{_libdir}/*.so

%files devel
%{_libdir}/*.a
%{_includedir}/uvm-systemc
%{_datadir}/pkgconfig/*.pc

%changelog
* Sat Aug 10 2024 Alex Fan <alex.fan.q@gmail.com> - 1.0-beta6-1
- Initial packaging of UVM-SystemC.

