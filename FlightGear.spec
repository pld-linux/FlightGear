Summary:	Free Flight Simulator
Summary(pl):	darmowy symulator lotu
Name:		FlightGear
Version:	0.9.4
Release:	2
License:	GPL
Group:		X11/Applications/Games
Source0:	ftp://ftp.flightgear.org/pub/fgfs/Source/%{name}-%{version}.tar.gz
# Source0-md5:	c815fd8117ebad44db2c9e0fe868cf26
Source1:	ftp://ftp.flightgear.org/pub/fgfs/Shared/fgfs-base-%{version}.tar.bz2
# Source1-md5:	9dcb351455b13cd8892612f69d6285fe
Source2:	ftp://ftp.flightgear.org/pub/fgfs/Everything-0.7/Base-Packages/fgfs-docs-0.7.7.tar.gz
# Source2-md5:	31f35d3e63e522565e8990ead99e7507
Patch0:		%{name}-libs.patch
URL:		http://www.flightgear.org/
BuildRequires:	OpenGL-devel
BuildRequires:	SimGear-devel >= 0.3.5
BuildRequires:	XFree86-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	findutils
BuildRequires:	glut-devel
BuildRequires:	libstdc++-devel
BuildRequires:	metakit-devel >= 2.4.3
BuildRequires:	plib-devel >= 1.8.0
BuildRequires:	zlib-devel
Requires:	OpenGL
Requires:	SimGear >= 0.3.4-2
Requires:	plib >= 1.8.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define _noautoreqdep	libGL.so.1 libGLU.so.1 libGLcore.so.1

%description
The Flight Gear project is working to create a sophisticated flight
simulator framework for the development and pursuit of interesting
flight simulator ideas. We are developing a solid basic sim that can
be expanded and improved upon by anyone interested in contributing.

%description -l pl
Projet Flight Gear to wyrafinowany symulator lotów pozwalaj±cy
rozpowszechniaæ idee tego typu symulacji.

%prep
%setup -q -a 1 -a 2
%patch0 -p1
find %{name} -name 'CVS' -type d | xargs rm -rf

%build
rm -f missing
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--with-network-olk \
	--with-multiplayer \
	--libdir=%{_datadir}/games
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/games

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

echo "#!/bin/sh" > runfgfs
echo "exec %{_bindir}/fgfs --fg-root=%{_datadir}/games/%{name} \$*" >> runfgfs
install runfgfs $RPM_BUILD_ROOT%{_bindir}
cp -a %{name} $RPM_BUILD_ROOT%{_datadir}/games
cp -R %{name}-%{version}/* $RPM_BUILD_ROOT%{_datadir}/games/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS %{name}/Docs/*
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%{_datadir}/games/%{name}
%{_mandir}/*/*
