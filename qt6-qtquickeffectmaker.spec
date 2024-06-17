%global qt_module qtquickeffectmaker

#global examples 1

#global unstable 1
%if 0%{?unstable}
%global prerelease rc2
%endif

Summary: Qt6 - Quick EffectMaker Tool 
Name:    qt6-%{qt_module}
Version: 6.7.1
Release: 1%{?dist}

# See LICENSE.GPL LICENSE.LGPL LGPL_EXCEPTION.txt, for details
# See also http://doc.qt.io/qt-5/licensing.html
License: GPLv3 with exceptions
Url:     http://www.qt.io
%global majmin %(echo %{version} | cut -d. -f1-2)
%global  qt_version %(echo %{version} | cut -d~ -f1)

%if 0%{?unstable}
Source0: https://download.qt.io/development_releases/qt/%{majmin}/%{qt_version}/submodules/%{qt_module}-everywhere-src-%{qt_version}-%{prerelease}.tar.xz
%else
Source0: https://download.qt.io/official_releases/qt/%{majmin}/%{version}/submodules/%{qt_module}-everywhere-src-%{version}.tar.xz
%endif
#Patch0:  qtquick3d-fix-build-with-gcc11.patch

BuildRequires: cmake
BuildRequires: gcc-c++
BuildRequires: ninja-build
BuildRequires: qt6-rpm-macros >= %{version}
BuildRequires: qt6-qtbase-static >= %{version}
BuildRequires: qt6-qtbase-private-devel
%{?_qt6:Requires: %{_qt6}%{?_isa} = %{_qt6_version}}
BuildRequires: qt6-qtdeclarative-devel
BuildRequires: qt6-qtdeclarative-static
BuildRequires: qt6-qtshadertools-devel
BuildRequires: qt6-qtquick3d-devel

%description
The Qt 6 Quick Effect Maker 

%if 0%{?examples}
%package examples
Summary: Programming examples for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
%description examples
%{summary}.
%endif

%prep
%autosetup -n %{qt_module}-everywhere-src-%{qt_version}%{?unstable:-%{prerelease}} -p1


%build

%cmake_qt6 \
        -DQT_BUILD_EXAMPLES=%{?examples:ON}%{!?examples:OFF}

%cmake_build


%install
%cmake_install

# hardlink files to %{_bindir}, add -qt6 postfix to not conflict
mkdir %{buildroot}%{_bindir}
pushd %{buildroot}%{_qt6_bindir}
for i in * ; do
  case "${i}" in
    qqem)
      ln -v  ${i} %{buildroot}%{_bindir}/${i}-qt6
      ;;
    *)
      ln -v  ${i} %{buildroot}%{_bindir}/${i}
      ;;
  esac
done
popd

%ldconfig_scriptlets

%files
%license LICENSES/*
%{_bindir}/qqem-qt6
%{_qt6_bindir}/qqem
%{_qt6_qmldir}/QtQuickEffectMaker/

%if 0%{?examples}
%files examples
%{_qt6_examplesdir}/
%endif


%changelog
* Mon Jun 17 2024 Alex Fan <alex.fan.q@gmail.com> - 6.7.1-1
- 6.7.1
- import from copr loise/qt6-6.7.0

* Fri Apr 05 2024 Marie Loise Nolden <loise@kde.org> - 6.7.0-1
- 6.7.0

* Fri Dec 08 2023 Marie Loise Nolden <loise@kde.org> - 6.6.1-1
- 6.6.1

* Thu May 25 2023 Marie Loise Nolden <loise@kde.org> - 6.5.1-1
- 6.5.1

* Tue Apr 4 2023 Marie Loise Nolden <loise@kde.org> - 6.5.0-1
- 6.5.0

