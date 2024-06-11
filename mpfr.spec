Name:       mpfr

Summary:    A C library for multiple-precision floating-point computations
Version:    4.2.1
Release:    1
License:    LGPLv3+ and GPLv3+ and GFDL
URL:        http://www.mpfr.org/
Source0:    %{name}-%{version}.tar.xz
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

%prep
%autosetup -p1

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

%install

%make_install
rm -f %{buildroot}%{_libdir}/*.la
rm -f %{buildroot}%{_infodir}/dir

#these go into licenses, not doc
rm -f %{buildroot}%{_pkgdocdir}/COPYING{,.LESSER}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%license COPYING COPYING.LESSER
%{_libdir}/libmpfr.so.6*

%files devel
%doc %{_docdir}/%{name}
%doc NEWS README AUTHORS BUGS TODO doc/FAQ.html
%{_libdir}/libmpfr.so
%{_includedir}/*.h
%{_libdir}/pkgconfig/mpfr.pc
%exclude %{_infodir}/mpfr.info.gz
