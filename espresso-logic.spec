%global pkgvers 1
%global schash0 6d5fc9a38a0fd308cff86df20389ac5c45ea2640
%global scdate0 20210807
%global branch0 main
%global source0 https://github.com/Gigantua/Espresso.git
%global sshort0 %{expand:%%{lua:print(('%{schash0}'):sub(1,8))}}

Name:           espresso-logic
Version:        2.3
Release:        %{scdate0}.%{pkgvers}.git%{sshort0}%{?dist}
Summary:        The espresso PLA logic minimization program made C++20 Windows 10 compatible
Group:          Development Tools

License:        MIT
URL:            https://github.com/Gigantua/Espresso

Patch0:		https://raw.githubusercontent.com/alexfanqi/copr-alexfanqi-personal/master/espresso-strdup.patch

BuildRequires:  gcc git

%global debug_package %{nil}

%description
Espresso heuristic logic minimizer made C++20 Windows 10 compatible - University of California, Berkeley.

%prep
git clone --depth 1 -n -b %{branch0} %{source0} .
git fetch --depth 1 origin %{schash0}
git reset --hard %{schash0}
git log --format=fuller

%patch 0 -p1

%build
%make_build -C ./src

%install
mkdir -p %{buildroot}%{_bindir}
install -m 0755 "./bin/espresso" %{buildroot}%{_bindir}/

%files
%{_bindir}/*
%license LICENSE
%doc README.md


%changelog
* Mon Jul 01 2024 Alex Fan <alex.fan.q@gmail.com>
- initial import
