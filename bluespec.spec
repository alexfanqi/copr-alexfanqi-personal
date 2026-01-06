# a large portion is brought from the gentoo guru ebuild:
# https://gitweb.gentoo.org/repo/proj/guru.git/tree/sci-electronics/bluespec/bluespec-9999.ebuild

%global pkg_name bluespec
%global pkgver %{pkg_name}-%{version}
%global shortname bsc
%{?haskell_setup}

%global yices2 Yices-2.6.4

# testsuite missing deps:
#

Name:           %{pkg_name}
Version:        2025.07
Release:        %autorelease
Summary:        Compiler, simulator, and tools for the Bluespec Hardware Description Language

License:        BSD-3-Clause
Url:            https://github.com/B-Lang-org/bsc
Source0:        %{URL}/archive/%{version}/%{name}-%{version}.tar.gz
Source10:       https://github.com/SRI-CSL/yices2/archive/%{yices2}.tar.gz
Patch0:         https://github.com/B-Lang-org/bsc/pull/278.patch

# base and integer-gmp
BuildRequires:  ghc-base-devel

BuildRequires:  ghc-containers-devel
BuildRequires:  ghc-array-devel
BuildRequires:  ghc-mtl-devel
BuildRequires:  ghc-unix-devel
BuildRequires:  ghc-regex-compat-devel
BuildRequires:  ghc-bytestring-devel
BuildRequires:  ghc-directory-devel
BuildRequires:  ghc-process-devel
BuildRequires:  ghc-filepath-devel
BuildRequires:  ghc-time-devel
BuildRequires:  ghc-old-time-devel
BuildRequires:  ghc-old-locale-devel
BuildRequires:  ghc-split-devel
BuildRequires:  ghc-syb-devel
BuildRequires:  ghc-text-devel
BuildRequires:  flex
BuildRequires:  bison
BuildRequires:  pkgconfig(tcl)
BuildRequires:  autoconf
BuildRequires:  gperf
BuildRequires:  g++
# vendored
# BuildRequires:  stp-devel
# BuildRequires:  yices-devel
BuildRequires:  vim-filesystem
BuildRequires:  rubygem-asciidoctor
BuildRequires:  rubygem-asciidoctor-pdf
BuildRequires:  texlive-collection-bibtexextra
BuildRequires:  texlive-collection-fontsextra
BuildRequires:  texlive-collection-fontutils
BuildRequires:  texlive-collection-latex
BuildRequires:  texlive-collection-latexextra
BuildRequires:  texlive-collection-latexrecommended
BuildRequires:  texlive-collection-plaingeneric

Requires:       tcsh
Requires:       tcl

Recommends:     ghc
Recommends:     zlib-devel

%global debug_package %{nil}

%description
Bluespec is a single language for digital electronic hardware designs
that comes in two syntactic flavors, which are interchangeable:
Bluespec SystemVerilog (BSV)
Bluespec Haskell (BH, or "Bluespec Classic").


%package doc
Summary:        documentation for bluespec
%description doc

documentation and release note for bluespec.


%prep
%setup -n bsc-%{version} -a10 -q
%patch 0 -p1 -b .orig
sed -i "s|ABSNAME=.*\$|ABSNAME=\$(readlink -f -- \"\$0\")|g" src/comp/wrapper.sh
rm -r src/vendor/yices/v2.6/yices2
ln -sr yices2-%{yices2} src/vendor/yices/v2.6/yices2


%build
# NO_DEPS_CHECKS=1: skip the subrepo check (this deriviation uses yices.src instead of the subrepo)
# LDCONFIG=ldconfig: https://github.com/B-Lang-org/bsc/pull/43
# STP_STUB=1: https://github.com/B-Lang-org/bsc/pull/278
%make_build NO_DEPS_CHECKS=1 LDCONFIG=ldconfig STP_STUB=1 install-src install-release install-doc
%make_build -C src/comp install-extra


%global _bsc_inst_path %{_datadir}/%{shortname}/%{shortname}-%{version}

%install
# upstream recommends placing the inst directory at /usr/share/bsc/bsc-<VERSION>
# https://github.com/B-Lang-org/bsc/blob/main/INSTALL.md
mkdir -p %{buildroot}%{_bsc_inst_path}
cp -dr --preserve=mode,timestamp inst/* %{buildroot}%{_bsc_inst_path}
mkdir -p %{buildroot}%{_bindir}
ln -sr %{buildroot}%{_bsc_inst_path}/bin/{bsc,bluetcl,bsc2bsv,bsv2bsc,dumpbo,dumpba,vcdcheck,showrules} %{buildroot}%{_bindir}/

# vim plugins
mkdir -p                                %{buildroot}%{vimfiles_root}
cp -r util/vim/{ftdetect,indent,syntax} %{buildroot}%{vimfiles_root}

%files
%doc README.md
%{_bindir}/*
%{_bsc_inst_path}/bin
%{_bsc_inst_path}/lib
%{vimfiles_root}/ftdetect/
%{vimfiles_root}/indent/
%{vimfiles_root}/syntax/

%files doc
%license %{_bsc_inst_path}/COPYING
%license %{_bsc_inst_path}/LICENSES/LICENSE.*
%doc %{_bsc_inst_path}/ReleaseNotes.*
%doc %{_bsc_inst_path}/README
%doc %{_bsc_inst_path}/doc


%changelog
* Tue Jan 06 2026 Alex Fan <alex.fan.q@gmail.com> - 2025.07
- bump to 2025.07

* Thu Mar 07 2025 Alex Fan <alex.fan.q@gmail.com> - 2024.07
- bump to 2024.07

* Thu Jul 18 2024 Alex Fan <alex.fan.q@gmail.com> - 2024.01
- initial package for Fedora
