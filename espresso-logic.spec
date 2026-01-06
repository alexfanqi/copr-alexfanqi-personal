Name:           espresso-logic
Version:        2.4
Release:        %autorelease
Summary:        A tool to produce a minimal equivalent representation of a Boolean function
Group:          Development/Tools

# The original Berkeley code is typically BSD-style. 
# Chipsalliance repo generally follows standard open source compatible licenses.
License:        BSD
URL:            https://github.com/chipsalliance/espresso/
Source0:        %{url}/archive/v%{version}/espresso-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  cmake
BuildRequires:  make

# If this package replaces an older generic 'espresso' package
Provides:       espresso = %{version}-%{release}

%description
Espresso is a heuristic logic minimizer. It takes as input a two-level 
representation of a two-valued or multiple-valued Boolean function 
and produces a minimal equivalent representation.

%prep
%autosetup -n espresso-%{version}

%build
export CFLAGS="%{optflags} -std=c99"

%cmake
%cmake_build

%install
%cmake_install

%check
%ctest

%files
%{_bindir}/espresso
%{_mandir}/man1/espresso.1*
%{_mandir}/man5/espresso.5*

%changelog
* Tue Jan 06 2026 Alex Fan <alex.fan.q@gmail.com> - 2.4-1
- Update to version 2.4 based on chipsalliance upstream
