# TODO:
# - Make FlightGear-extra-planes for subset of planes from
#   http://www.flightgear.org/Downloads/aircraft/index.shtml

#
# Conditional build:
%bcond_without	data		# don't build data package (for quick test build)
#
Summary:	Free Flight Simulator
Summary(pl.UTF-8):	darmowy symulator lotu
Name:		FlightGear
Version:	3.2.0
Release:	3
License:	GPL
Group:		X11/Applications/Games
Source0:	ftp://mirrors.ibiblio.org/pub/mirrors/flightgear/ftp/Source/flightgear-%{version}.tar.bz2
# Source0-md5:	0a16920cc22ea070f8bb345e76c55e05
Source1:	ftp://mirrors.ibiblio.org/pub/mirrors/flightgear/ftp/Shared/%{name}-data-%{version}.tar.bz2
# Source1-md5:	24774fae7199bcbc5e23672f4a586884
#Source2:	ftp://ftp.flightgear.org/pub/fgfs/Everything-0.7/Base-Packages/fgfs-docs-0.7.7.tar.gz
## Source2-md5:	31f35d3e63e522565e8990ead99e7507
Patch0:		flightgear-cmake.patch
Patch1:		OpenSceneGraph-3.3.2.patch
Patch2:		rtti-fix.patch
URL:		http://www.flightgear.org/
BuildRequires:	OpenAL-devel
BuildRequires:	OpenGL-devel
BuildRequires:	OpenSceneGraph-devel
BuildRequires:	SimGear-devel = %{version}
BuildRequires:	cmake
BuildRequires:	flite-devel
BuildRequires:	fltk-gl-devel
BuildRequires:	freeglut-devel
BuildRequires:	libgsm-devel
BuildRequires:	libstdc++-devel
BuildRequires:	speex-devel
BuildRequires:	sqlite3-devel
BuildRequires:	plib-devel >= 1.8.5-3
BuildRequires:	zlib-devel
Requires:	%{name}-data = %{version}
Requires:	OpenGL
Requires:	OpenSceneGraph-plugins
Requires:	plib >= 1.8.4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoreqdep	libGL.so.1 libGLU.so.1 libGLcore.so.1

%description
The Flight Gear project is working to create a sophisticated flight
simulator framework for the development and pursuit of interesting
flight simulator ideas. We are developing a solid basic sim that can
be expanded and improved upon by anyone interested in contributing.

%description -l pl.UTF-8
Projekt Flight Gear to wyrafinowany symulator lotów pozwalający
rozpowszechniać idee tego typu symulacji.

%package data
Summary:	FlightGear base scenery and data files
License:	GPL v2+
Group:		Applications/Games
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description data
This package contains the base scenery for FlightGear and must be
installed

%prep
%setup -q -n flightgear-%{version} %{?with_data:-a 1}
%patch0 -p1
%patch1 -p1
%patch2 -p1

cat > runfgfs <<'EOF'
#!/bin/sh
exec %{_bindir}/fgfs --fg-root=%{_datadir}/games/%{name}/fgdata "$@"
EOF

%build
install -d build
cd build
%cmake .. \
	-DSYSTEM_SQLITE:BOOL=ON

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/games/%{name}

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

install -p runfgfs $RPM_BUILD_ROOT%{_bindir}
%if %{with data}
cp -a fgdata $RPM_BUILD_ROOT%{_datadir}/games/%{name}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS docs-mini/*
%attr(755,root,root) %{_bindir}/*
%{_mandir}/*/*

%if %{with data}
%files data
%defattr(644,root,root,755)
%{_datadir}/games/%{name}
%endif
