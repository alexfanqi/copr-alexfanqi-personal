Name:           ccls
Version:        0.20220729
Release:        %autorelease
Summary:        C/C++/ObjC language server supporting cross references, hierarchies, completion and semantic highlighting
Group:          Development Tools

License:        Apache-2.0 AND CC0-1.0 AND BSL-1.0
URL:            https://github.com/MaskRay/ccls
Source0:        %{URL}/archive/%{version}/%{name}-%{version}.tar.gz
Patch0:         %{URL}/commit/6dc564f2a8608fff778a7d7e8ed0d5acd8d61e6b.patch#/llvm16-optional-deprecation.patch
Patch1:         %{URL}/commit/ba38e13b93de1e8787b7e8a22b9a00d35b2b40f2.patch#/llvm17-precompiled-preamble-build.patch

BuildRequires:  cmake >= 3.8
BuildRequires:  clang-devel >= 7.0
BuildRequires:  llvm-devel >= 7.0
BuildRequires:  zlib-devel
BuildRequires:  rapidjson-devel
Requires:       clang >= 5.0
Requires:       llvm >= 7.0
Provides:       bundled(macro_map)
Provides:       bundled(siphash)

%global debug_package %{nil}

%description
ccls, which originates from cquery, is a C/C++/Objective-C language server.

It has a global view of the code base and support a lot of cross reference features, see wiki/FAQ. It starts indexing the whole project (including subprojects if exist) parallelly when you open the first file, while the main thread can serve requests before the indexing is complete. Saving files will incrementally update the index.

Compared with cquery, it makes use of C++17 features, has less third-party dependencies and slimmed-down code base. It leverages Clang C++ API as clangd does, which provides better support for code completion and diagnostics. Refactoring is a non-goal as it can be provided by clang-include-fixer and other Clang based tools.


%prep
%autosetup -p1
rm -rf third_party/rapidjson

%build
%cmake -DLLVM_ENABLE_RTTI=on \
  -DLLVM_LINK_LLVM_DYLIB=ON \
  -DCLANG_LINK_CLANG_DYLIB=ON \
  -DUSE_SYSTEM_RAPIDJSON=ON
%cmake_build

%install
%cmake_install

%files
%{_bindir}/%{name}
%license LICENSE
%doc README.md


%changelog
* Mon Nov  20 2023 Alex Fan <alex.fan.q@gmail.com>
- Update to ccls 0.20220729
- Backport upstream patch llvm17-precompiled-preamble-build.patch
  to fix build with LLVM 17
- Backport upstream patch llvm16-optional-deprecation.patch to fix
  build with LLVM 16.

* Mon Nov  12 2018 Yotam Nachum <fedora@yotam.net>
- Initial Fedora package
