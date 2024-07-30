%global lockver 1
%global pkgvers 0
%global scdate0 20230801
%global schash0 12fc549c4892b13bf17c61ecb814119f45d0bf50
%global sctags0 firtool-1.49.0
%global source0 https://github.com/llvm/circt.git

%define with_python 0
%define with_ortool 0

Name:           circt
Version:        %(echo "%{sctags0}" | sed 's|[^0-9,\.]||g')
Release:        %{scdate0}.%{pkgvers}%{?dist}
Summary:        Circuit IR Compilers and Tools
License:        Apache 2.0

URL:            https://circt.llvm.org

Patch0:         circt-1.49.0.patch

BuildRequires:  cmake git gcc-c++ clang-tools-extra capnproto
BuildRequires:  zlib-devel ncurses-devel z3-devel capnproto-devel
BuildRequires:  libffi-devel gtest-devel verilator iverilog yosys
BuildRequires:  llvm-devel >= 17
BuildRequires:  mlir-devel >= 17
%if %{with_ortool}
BuildRequires:   or-tools-devel
%endif

%global __cmake_in_source_build 1

%description
"CIRCT" stands for "Circuit IR Compilers and Tools".

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description    devel
This package contains development files for %{name}.

%if %{with_python}
%package        python3
Summary:        Python files for %{name}
Requires:       %{name} = %{version}-%{release}

%description    python3
This package contains python files for %{name}.
%endif


%prep
%setup -T -c -n %{name}
find %{_builddir} -name SPECPARTS -exec rm -rf {} +
git clone --depth 1 -n -b %{sctags0} %{source0} .
git reset --hard %{sctags0}
git log --format=fuller
%autosetup -D -p 1 -T -c -n %{name}
# python
sed -i 's|message(FATAL_ERROR "CIRCT Python bindings|message(WARNING "CIRCT Python bindings|' CMakeLists.txt


%build
mkdir build
pushd build
%global optflags $(echo "%{optflags} -fpermissive")
%cmake .. -Wno-dev \
       -DCMAKE_SKIP_RPATH=ON \
       -DCMAKE_VERBOSE_MAKEFILE=OFF \
       -DCMAKE_BUILD_TYPE=RelWithDebInfo \
%if %{with_ortool}
       -DOR_TOOLS_DISABLE=OFF \
%else
       -DOR_TOOLS_DISABLE=ON \
%endif
%if %{with_python}
       -DCIRCT_BINDINGS_PYTHON_ENABLED=ON
%else
       -DCIRCT_BINDINGS_PYTHON_ENABLED=OFF
%endif
make %{?_smp_mflags}
popd


%install
# build
pushd build
%cmake_install
popd


%files
%license LICENSE
%doc README.md
%{_bindir}/*
%{_libdir}/lib*.so.*

%files devel
%{_includedir}/*
%{_libdir}/lib*.so
%{_libdir}/cmake/%{name}

%if %{with_python}
%files python3
%{python3_sitearch}/*
%endif


%changelog
* Wed Jul 12 2023 Balint Cristian <cristian.balint@gmail.com>
- github update releases
