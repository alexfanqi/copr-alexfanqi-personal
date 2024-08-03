%global lockver 1
%global pkgvers 0
%global scdate0 20240204
%global schash0 cd2a0518f4a7915a37c52aa8c6bf4a236573403e
# lastest version that can be built with mlir-18
# newer version has conflicts:
# lib/Conversion/LLHDToLLVM/LLHDToLLVM.cpp:func.addEntryBlock(moduleBuilder)
# lib/Dialect/Arc/Transforms/ArcCanonicalizer.cpp:void notifyOperationInserted(Operation *op, mlir::IRRewriter::InsertPoint) override
%global sctags0 firtool-1.65.0
%global source0 https://github.com/llvm/circt.git

%define with_ortool 0
%define unified_build 0
%define with_python 0

Name:           circt
Version:        %(echo "%{sctags0}" | sed 's|[^0-9,\.]||g')
Release:        %{scdate0}.%{pkgvers}%{?dist}
Summary:        Circuit IR Compilers and Tools
License:        Apache 2.0

URL:            https://circt.llvm.org
# hack to work around https://github.com/llvm/llvm-project/issues/68546
Patch0:         https://github.com/alexfanqi/copr-alexfanqi-personal/raw/master/circt-hack-mlir-linalg-ods-yaml-gen.patch
Patch1:         https://github.com/alexfanqi/copr-alexfanqi-personal/raw/master/circt-install-dir.patch
Patch2:         https://github.com/alexfanqi/copr-alexfanqi-personal/raw/master/circt-mlir-tblgen-path.patch
Patch3:         https://github.com/alexfanqi/copr-alexfanqi-personal/raw/master/circt-skip-integration-test.patch

BuildRequires:  cmake git gcc-c++ clang-tools-extra capnproto
BuildRequires:  zlib-devel ncurses-devel z3-devel capnproto-devel
BuildRequires:  libffi-devel
BuildRequires:  python3-lit >= 18
%if ! %{unified_build}
BuildRequires:  mlir-devel >= 18
BuildRequires:  llvm-devel >= 18
%endif
%if %{with_python}
BuildRequires:  python3-devel
BuildRequires:  python3-devel
BuildRequires:  python3-numpy
BuildRequires:  python3-pybind11
BuildRequires:  python3-pyyaml
%endif
%if %{with_ortool}
BuildRequires:  or-tools-devel
%endif
Recommends: verilator iverilog yosys

%global __cmake_in_source_build 0

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
%if %{unified_build}
git submodule init .
git submodule update
%autosetup -D -p 1 -T -c -n %{name}
%else
%patch -P 1 -p1
%patch -P 2 -p1
%patch -P 3 -p1
%autosetup -D -N -T -c -n %{name}
%endif
# python
sed -i 's|message(FATAL_ERROR "CIRCT Python bindings|message(WARNING "CIRCT Python bindings|' CMakeLists.txt


%build
mkdir build
pushd build
%global optflags $(echo "%{optflags} -fpermissive")
%global my_cmake_flags %{shrink:
       -D CMAKE_SKIP_RPATH=ON
       -D CMAKE_VERBOSE_MAKEFILE=OFF
       -D CMAKE_BUILD_TYPE=RelWithDebInfo
       -D LLVM_EXTERNAL_LIT=%{_bindir}/lit
       -D CIRCT_BUILD_TOOLS=ON
}

%if %{with_ortool}
%define my_ortool_flags -D OR_TOOLS_DISABLE=OFF
%else
%define my_ortool_flags -D OR_TOOLS_DISABLE=ON
%endif

%if %{unified_build}
%cmake -S ../llvm/llvm -Wno-dev \
        %{my_cmake_flags} %{my_ortool_flags} \
       -D LLVM_ENABLE_PROJECTS=mlir \
       -D BUILD_SHARED_LIBS=OFF \
       -D LLVM_STATIC_LINK_CXX_STDLIB=ON \
       -D LLVM_ENABLE_ASSERTIONS=ON \
       -D LLVM_BUILD_EXAMPLES=OFF \
       -D LLVM_ENABLE_BINDINGS=OFF \
       -D LLVM_ENABLE_OCAMLDOC=OFF \
       -D LLVM_EXTERNAL_PROJECTS=circt \
       -D LLVM_EXTERNAL_CIRCT_SOURCE_DIR="${PWD}/.." \
%if %{with_python}
       -D CIRCT_BINDINGS_PYTHON_ENABLED=ON \
       -D CIRCT_ENABLE_FRONTENDS=PyCDE \
       -D MLIR_ENABLE_BINDINGS_PYTHON=ON
%else
       -D CIRCT_BINDINGS_PYTHON_ENABLED=OFF \
       -D MLIR_ENABLE_BINDINGS_PYTHON=OFF
%endif
%else
%cmake -S .. -Wno-dev \
        %{my_cmake_flags} %{my_ortool_flags}
%endif
%cmake_build
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
%{python3_sitearch}/circt
%endif


%changelog
* Tue Jul 30 2024 Alex Fan <alex.fan.q@gmail.com>
- bump to tag firtool 1.67.0
- migrate to unified build
- enable building python binding, still broken
* Wed Jul 12 2023 Balint Cristian <cristian.balint@gmail.com>
- github update releases
