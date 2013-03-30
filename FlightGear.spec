# TODO:
# - Make FlightGear-extra-planes for subset of planes from
#   http://www.flightgear.org/Downloads/aircraft/index.shtml

Summary:	Free Flight Simulator
Summary(pl.UTF-8):	darmowy symulator lotu
Name:		FlightGear
Version:	2.10.0
Release:	1
License:	GPL
Group:		X11/Applications/Games
Source0:	ftp://mirrors.ibiblio.org/pub/mirrors/flightgear/ftp/Source/flightgear-%{version}.tar.bz2
# Source0-md5:	ae7fc8d1e446c5d1fe2aa82ee41dcac5
Source1:	ftp://flightgear.wo0t.de/ftp/Shared/FlightGear-data-%{version}.tar.bz2
# Source1-md5:	82a9cbc81313195a7ed1aa87a9a2a0b3
#Source2:	ftp://ftp.flightgear.org/pub/fgfs/Everything-0.7/Base-Packages/fgfs-docs-0.7.7.tar.gz
## Source2-md5:	31f35d3e63e522565e8990ead99e7507
Patch0:		flightgear-cmake.patch
Patch1:		flightgear-shader.patch
URL:		http://www.flightgear.org/
BuildRequires:	cmake
BuildRequires:	OpenAL-devel
BuildRequires:	OpenGL-devel
BuildRequires:	SimGear-devel = %{version}
BuildRequires:	freeglut-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libxml-devel
BuildRequires:	plib-devel >= 1.8.5-3
BuildRequires:	zlib-devel
Requires:	OpenGL
Requires:	OpenSceneGraph-plugins
Requires:	plib >= 1.8.4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define _noautoreqdep	libGL.so.1 libGLU.so.1 libGLcore.so.1

%description
The Flight Gear project is working to create a sophisticated flight
simulator framework for the development and pursuit of interesting
flight simulator ideas. We are developing a solid basic sim that can
be expanded and improved upon by anyone interested in contributing.

%description -l pl.UTF-8
Projekt Flight Gear to wyrafinowany symulator lotów pozwalający
rozpowszechniać idee tego typu symulacji.

%prep
%setup -q -n flightgear-%{version} -a 1
%patch0 -p1
%patch1 -p1

find %{name} -name 'CVS' -type d | xargs rm -rf

%build
install -d build
cd build
%cmake ../
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/games/%{name}

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

echo "#!/bin/sh" > runfgfs
echo "exec %{_bindir}/fgfs --fg-root=%{_datadir}/games/%{name} \$*" >> runfgfs
install runfgfs $RPM_BUILD_ROOT%{_bindir}
cp -R data $RPM_BUILD_ROOT%{_datadir}/games/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS docs-mini/*
%attr(755,root,root) %{_bindir}/*
%{_datadir}/games/%{name}
%{_mandir}/*/*
