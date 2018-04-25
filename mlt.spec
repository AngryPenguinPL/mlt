%define major 6
%define plusmaj 3
%define libname %mklibname %{name} %{major}
%define libplus %mklibname mlt++ %{plusmaj}
%define devname %mklibname %{name} -d
%define _disable_lto 1

%bcond_with mmx

Summary:	Media Lovin' Toolkit nonlinear video editing library
Name:		mlt
Version:	6.4.1
Release:	4
License:	LGPLv2+
Group:		Video
Url:		http://mlt.sourceforge.net
Source0:	http://downloads.sourceforge.net/project/mlt/mlt/%{name}-%{version}.tar.gz
Patch1:		mlt-0.9.2-py3.patch
Patch2:		mlt-inline-asm-lto.patch
Patch3:		mlt-6.4.1-glibc-2.26.patch
Patch6:		mlt-6.4.1-crash_fix.patch
BuildRequires:	imagemagick
BuildRequires:	ffmpeg
BuildRequires:	ffmpeg-devel
BuildRequires:	ladspa-devel
BuildRequires:	pkgconfig(Qt5Core)
BuildRequires:	pkgconfig(Qt5Gui)
BuildRequires:	pkgconfig(Qt5OpenGL)
BuildRequires:	pkgconfig(Qt5Svg)
BuildRequires:	pkgconfig(Qt5Widgets)
BuildRequires:	pkgconfig(Qt5Xml)
BuildRequires:	pkgconfig(libexif)
BuildRequires:	pkgconfig(eigen3)
BuildRequires:	pkgconfig(fftw3)
BuildRequires:	pkgconfig(epoxy)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(frei0r)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(jack)
BuildRequires:	pkgconfig(libdv)
BuildRequires:	pkgconfig(libquicktime)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(mad)
BuildRequires:	pkgconfig(movit)
BuildRequires:	pkgconfig(ogg)
BuildRequires:	pkgconfig(pango)
BuildRequires:	pkgconfig(samplerate)
BuildRequires:	pkgconfig(sdl)
BuildRequires:	pkgconfig(sox)
BuildRequires:	pkgconfig(vorbis)
BuildRequires:	pkgconfig(opencv)
# For python-bindings
BuildRequires:	swig
BuildRequires:	pkgconfig(python)

%description
MLT is an open source multimedia framework, designed and developed for
television broadcasting.

It provides a toolkit for broadcasters, video editors, media players,
transcoders, web streamers and many more types of applications. The
functionality of the system is provided via an assortment of ready to
use tools, xml authoring components, and an extendible plug-in based
API.

%files
%doc docs COPYING README
%{_bindir}/melt
%{_datadir}/mlt
%{_libdir}/mlt

#----------------------------------------------------------------------------

%package -n %{libname}
Summary:	Main library for mlt
Group:		System/Libraries

%description -n %{libname}
This package contains the libraries needed to run programs dynamically
linked with mlt.

%files -n %{libname}
%{_libdir}/libmlt.so.%{major}*

#----------------------------------------------------------------------------

%package -n %{libplus}
Summary:	Main library for mlt++
Group:		System/Libraries

%description -n %{libplus}
This package contains the libraries needed to run programs dynamically
linked with mlt++.

%files -n %{libplus}
%{_libdir}/libmlt++.so.%{plusmaj}*
%{_libdir}/libmlt++.so.%{major}*

#----------------------------------------------------------------------------

%package -n %{devname}
Summary:	Headers for developing programs that will use mlt
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Requires:	%{libplus} = %{EVRD}
# mlt-config requires stuff from %{_datadir}/%{name}
Requires:	%{name} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n %{devname}
This package contains the headers that programmers will need to develop
applications which will use mlt.

%files -n %{devname}
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

#----------------------------------------------------------------------------

%package -n python-%{name}
Summary:	Python bindings for MLT
Group:		Development/Python
Requires:	python
Requires:	%{name} = %{EVRD}

%description -n python-%{name}
This module allows to work with MLT using python.

%files -n python-%{name}
%{py2_platsitedir}/%{name}.p*
%{py2_platsitedir}/_%{name}.so

#----------------------------------------------------------------------------

%prep
%setup -q
%patch1 -p0 -b .py3~
%patch2 -p1 -b .asm~
%patch3 -p1 -b .glibc226~
%patch6 -p1

%build
#export CC=gcc
#export CXX=g++
CXXFLAGS="%{optflags} -std=gnu++14" %configure \
	--disable-debug \
	--enable-gpl \
	--enable-gpl3 \
	--enable-opengl \
%if %{with mmx}
	--enable-mmx \
%else
	%ifarch x86_64
	--enable-mmx \
	--enable-sse \
	--enable-sse2 \
	%else
	--disable-mmx \
	--disable-sse \
	--disable-sse2 \
	%endif
%endif
	--luma-compress \
	--enable-avformat \
	--avformat-shared=%{_prefix} \
	--avformat-swscale \
	--enable-motion-est \
	--qt-libdir=%{_qt5_libdir} \
	--qt-includedir=%{_qt5_includedir} \
	--swig-languages='python'

%make

%install
%makeinstall_std
install -d %{buildroot}%{py2_platsitedir}
install -pm 0644 src/swig/python/%{name}.py* %{buildroot}%{py2_platsitedir}/
install -pm 0755 src/swig/python/_%{name}.so %{buildroot}%{py2_platsitedir}/

