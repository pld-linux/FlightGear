Summary:	Free Flight Simulator
Summary(pl):	darmowy symulator lotu
Name:		FlightGear
Version:	0.7.6
Release:	1
Group:		X11/Games
License:	GPL
Source0:	ftp://ftp.flightgear.org/pub/fgfs/Source/%{name}-%{version}.tar.gz
Source1:	ftp://ftp.flightgear.org/pub/fgfs/Shared/fgfs-base-%{version}.tar.gz
Source2:	ftp://ftp.flightgear.org/pub/fgfs/Shared/fgfs-docs-%{version}.tar.gz
Patch0:		%{name}-libs.patch
URL:		http://www.flightgear.org
Requires:	OpenGL
BuildRequires:	OpenGL-devel
BuildRequires:	XFree86-devel
BuildRequires:	libstdc++-devel
BuildRequires:	glut-devel
BuildRequires:	automake
BuildRequires:	autoconf
BuildRequires:	plib >= 1.2.0
BuildRequires:	SimGear-devel
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define _noautoreqdep	libGL.so.1 libGLU.so.1
%define _prefix		/usr/X11R6

%description

%description -l pl

%prep
%setup -q -a 1 -a 2
%patch0 -p1

%build
aclocal
autoconf
automake -a -c
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}
%{__make} DESTDIR="$RPM_BUILD_ROOT" install

echo "#!/bin/sh" > runfgfs
echo "exec %{_bindir}/fgfs --fg-root=%{_datadir}/%{name} \$*" >> runfgfs
install runfgfs $RPM_BUILD_ROOT%{_bindir}
cp -a %{name} $RPM_BUILD_ROOT%{_datadir}
find %{name}-0.7 -name 'CVS' -type d | xargs rm -rf

gzip -9nf AUTHORS NEWS

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc %{name}-0.7/docs/*
%doc *.gz
%attr(755,root,root) %{_bindir}/fgfs
%attr(755,root,root) %{_bindir}/runfgfs
%{_datadir}/%{name}
