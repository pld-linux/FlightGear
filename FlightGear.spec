Summary:	Free Flight Simulator
Summary(pl):	darmowy symulator lotu
Name:		FlightGear
Version:	0.8.0
Release:	1
License:	GPL
Group:		X11/Applications/Games
Source0:	ftp://ftp.flightgear.org/pub/fgfs/Source/%{name}-%{version}.tar.gz
Source1:	ftp://ftp.flightgear.org/pub/fgfs/Shared/fgfs-base-%{version}.tar.gz
Source2:	ftp://ftp.flightgear.org/pub/fgfs/Shared/fgfs-docs-0.7.7.tar.gz
Patch0:		%{name}-libs.patch
URL:		http://www.flightgear.org/
BuildRequires:	OpenGL-devel
BuildRequires:	SimGear-devel >= 0.2.0
BuildRequires:	XFree86-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	findutils
BuildRequires:	glut-devel
BuildRequires:	libstdc++-devel
BuildRequires:	metakit-devel >= 2.4.3
BuildRequires:	plib >= 1.6.0
BuildRequires:	zlib-devel
Requires:	OpenGL
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
	--with-network-olk
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}

%{__make} DESTDIR="$RPM_BUILD_ROOT" install

echo "#!/bin/sh" > runfgfs
echo "exec %{_bindir}/fgfs --fg-root=%{_libdir}/%{name} \$*" >> runfgfs
install runfgfs $RPM_BUILD_ROOT%{_bindir}
cp -a %{name} $RPM_BUILD_ROOT%{_libdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS %{name}/Docs/*
%attr(755,root,root) %{_bindir}/fgfs
%attr(755,root,root) %{_bindir}/runfgfs
%attr(755,root,root) %{_bindir}/est-epsilon
%attr(755,root,root) %{_bindir}/fgjs
%attr(755,root,root) %{_bindir}/gl-info
%attr(755,root,root) %{_bindir}/js_demo
%{_libdir}/%{name}
%{_mandir}/*/*
