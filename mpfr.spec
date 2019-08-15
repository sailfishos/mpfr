Name:       mpfr

Summary:    A C library for multiple-precision floating-point computations
Version:    3.1.6
Release:    1
Group:      System/Libraries
License:    LGPLv3+ and GPLv3+ and GFDL
URL:        http://www.mpfr.org/
Source0:    http://www.mpfr.org/%{name}-%{version}/%{name}-%{version}.tar.xz
Patch0:     rev11783.patch
Patch1:     rev11982.patch
Requires:   gmp >= 4.2.3
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires:  gmp-devel >= 4.2.3

%description
The MPFR library is a C library for multiple-precision floating-point
computations with "correct rounding". The MPFR is efficient and
also has a well-defined semantics. It copies the good ideas from the
ANSI/IEEE-754 standard for double-precision floating-point arithmetic
(53-bit mantissa). MPFR is based on the GMP multiple-precision library.


%package devel
Summary:    Development tools A C library for mpfr library
Group:      Development/Libraries
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

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
%make_install
rm -f $RPM_BUILD_ROOT%{_libdir}/libmpfr.la
rm -f $RPM_BUILD_ROOT%{_infodir}/dir
	
#these go into licenses, not doc
rm -f $RPM_BUILD_ROOT%{_pkgdocdir}/COPYING  $RPM_BUILD_ROOT%{_pkgdocdir}/COPYING.LESSER

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%license COPYING COPYING.LESSER
%{_libdir}/libmpfr.so.*

%files devel
%defattr(-,root,root,-)
%doc %{_docdir}/%{name}
%doc NEWS README AUTHORS BUGS TODO doc/FAQ.html
%{_libdir}/libmpfr.so
%{_includedir}/*.h
%exclude %{_infodir}/mpfr.info.gz
