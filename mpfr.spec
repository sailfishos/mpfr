# MPFR versions 3 and 4 must exist in parallel until we can move all
# consumers to version 4.
%global mpfr3ver 3.1.6

Name:       mpfr

Summary:    A C library for multiple-precision floating-point computations
Version:    4.2.0
Release:    1
License:    LGPLv3+ and GPLv3+ and GFDL
URL:        http://www.mpfr.org/
Source0:    %{name}-%{version}.tar.xz
Source1:    %{name}-%{mpfr3ver}.tar.xz
Patch0:     allpatches.patch
Patch100:   rev11783.patch
Patch101:   rev11982.patch
Requires:   gmp >= 5.0
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires:  gmp-devel >= 5.0

%description
The MPFR library is a C library for multiple-precision floating-point
computations with "correct rounding". The MPFR is efficient and
also has a well-defined semantics. It copies the good ideas from the
ANSI/IEEE-754 standard for double-precision floating-point arithmetic
(53-bit mantissa). MPFR is based on the GMP multiple-precision library.

%package devel
Summary:    Development tools A C library for mpfr library
Requires:   %{name} = %{version}-%{release}
Requires: gmp-devel

%description devel
The static libraries, header files and documentation for using the MPFR
multiple-precision floating-point library in applications.

If you want to develop applications which will use the MPFR library,
you'll need to install the mpfr-devel package.  You'll also need to
install the mpfr package.

%package -n mpfr3
Version: %{mpfr3ver}
Summary: C library for multiple-precision floating point computations

%description -n mpfr3
The MPFR library is a C library for multiple-precision floating-point
computations with "correct rounding". The MPFR is efficient and
also has a well-defined semantics. It copies the good ideas from the
ANSI/IEEE-754 standard for double-precision floating-point arithmetic
(53-bit mantissa). MPFR is based on the GMP multiple-precision library.

%package -n mpfr3-devel
Version: %{mpfr3ver}
Summary: Development files for the MPFR library
Requires: mpfr3%{?_isa} = %{mpfr3ver}-%{release}
Requires: gmp-devel%{?_isa}

%description -n mpfr3-devel
Header files and documentation for using the MPFR
multiple-precision floating-point library in applications.

If you want to develop applications which will use the MPFR library,
you'll need to install the mpfr3-devel package. You'll also need to
install the mpfr3 package.

%prep
%setup -q
%setup -q -T -D -a 1
%patch0 -p1

# Apply mpfr3 patches
cd %{name}-%{mpfr3ver}
%patch100 -p1
%patch101 -p1
cd -

%build

%configure --disable-static \
    --disable-assert

# Get rid of undesirable hardcoded rpaths; workaround libtool reordering
# -Wl,--as-needed after all the libraries.
sed -e 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' \
    -e 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' \
    -e 's|CC="\(g..\)"|CC="\1 -Wl,--as-needed"|' \
    -i libtool

%make_build

# Build mpfr3
cd %{name}-%{mpfr3ver}
%configure --disable-assert --disable-static

# Get rid of undesirable hardcoded rpaths; workaround libtool reordering
# -Wl,--as-needed after all the libraries.
sed -e 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' \
    -e 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' \
    -e 's|CC="\(g..\)"|CC="\1 -Wl,--as-needed"|' \
    -i libtool

%make_build
cd -

%install
# Install mpfr3
cd %{name}-%{mpfr3ver}
%make_install
rm -fr %{buildroot}%{_infodir}
rm %{buildroot}%{_libdir}/libmpfr.so
ln -s libmpfr.so.4 %{buildroot}%{_libdir}/libmpfr3.so

# Fix up the documentation
mv %{buildroot}%{_datadir}/doc/mpfr %{buildroot}%{_docdir}/mpfr3
cp -p PATCHES README %{buildroot}%{_docdir}/mpfr3
rm -fr %{buildroot}%{_docdir}/mpfr3/{AUTHORS,examples,FAQ.html,TODO}

# These go into licenses, not doc
rm -f %{buildroot}%{_docdir}/mpfr3/COPYING{,.LESSER}

# Stay out of the way of mpfr 4
mv %{buildroot}%{_includedir}/mpf2mpfr.h %{buildroot}%{_includedir}/mpf2mpfr3.h
mv %{buildroot}%{_includedir}/mpfr.h %{buildroot}%{_includedir}/mpfr3.h
cd -

%make_install
rm -f %{buildroot}%{_libdir}/*.la
rm -f %{buildroot}%{_infodir}/dir

#these go into licenses, not doc
rm -f %{buildroot}%{_pkgdocdir}/COPYING{,.LESSER}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post -n mpfr3 -p /sbin/ldconfig

%postun -n mpfr3 -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%license COPYING COPYING.LESSER
%{_libdir}/libmpfr.so.6*

%files devel
%defattr(-,root,root,-)
%doc %{_docdir}/%{name}
%doc NEWS README AUTHORS BUGS TODO doc/FAQ.html
%{_libdir}/libmpfr.so
%{_includedir}/*.h
%{_libdir}/pkgconfig/mpfr.pc
%exclude %{_infodir}/mpfr.info.gz

%files -n mpfr3
%license COPYING COPYING.LESSER
%{_docdir}/mpfr3/BUGS
%{_docdir}/mpfr3/NEWS
%{_docdir}/mpfr3/PATCHES
%{_docdir}/mpfr3/README
%{_libdir}/libmpfr.so.4*

%files -n mpfr3-devel
%{_libdir}/libmpfr3.so
%{_includedir}/mpfr3.h
%{_includedir}/mpf2mpfr3.h
