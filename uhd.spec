%define	ver_major 3
%define	ver_minor 8
%define	ver_patch 3

%define	ver %(printf "%03d.%03d.%03d" %{ver_major} %{ver_minor} %{ver_patch})
Summary:	Universal Hardware Driver for Ettus Research products
Name:		uhd
Version:	%{ver_major}.%{ver_minor}.%{ver_patch}
Release:	0.1
License:	GPL v3+
Group:		X11/Libraries
Source0:	http://files.ettus.com/binaries/uhd/uhd_%{ver}-release/%{name}-%{version}.tar.gz
# Source0-md5:	84928825717678e77ffc400d73bcf412
URL:		http://www.qcustomplot.com/
BuildRequires:	QtCore-devel
BuildRequires:	QtGui-devel
BuildRequires:	boost-devel
BuildRequires:	cmake >= 2.8.0
BuildRequires:	doxygen
BuildRequires:	libusb-devel
BuildRequires:	ncurses-devel
BuildRequires:	orc-devel
BuildRequires:	pkgconfig
BuildRequires:	python-cheetah
BuildRequires:	qt4-build
BuildRequires:	rpm-pythonprov
BuildRequires:	udev-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		filterout	-flto

%description
The UHD is the universal hardware driver for Ettus Research products.
The goal of the UHD is to provide a host driver and API for current
and future Ettus Research products. It can be used standalone without
GNU Radio.

%package devel
Summary:	Development files for %{name}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for Universal Hardware Driver for Ettus Research
products.

%package doc
Summary:	Documentation and examples for uhd
Group:		Documentation
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description doc
Documentation and examples for Universal Hardware Driver for Ettus
Research products

%prep
%setup -q

%build
install -d build
cd build
%cmake \
	..
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C build install/fast \
	DESTDIR=$RPM_BUILD_ROOT

rm $RPM_BUILD_ROOT%{_libdir}/%{name}/utils/usrp_n2xx_simple_net_burner
rm $RPM_BUILD_ROOT%{_libdir}/%{name}/utils/usrp_x3xx_fpga_burner

# not packaged
rm -r $RPM_BUILD_ROOT%{_libdir}/%{name}/tests

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/nirio_programmer
%attr(755,root,root) %{_bindir}/octoclock_firmware_burner
%attr(755,root,root) %{_bindir}/uhd_cal_rx_iq_balance
%attr(755,root,root) %{_bindir}/uhd_cal_tx_dc_offset
%attr(755,root,root) %{_bindir}/uhd_cal_tx_iq_balance
%attr(755,root,root) %{_bindir}/uhd_find_devices
%attr(755,root,root) %{_bindir}/uhd_images_downloader
%attr(755,root,root) %{_bindir}/uhd_usrp_probe
%attr(755,root,root) %{_bindir}/usrp2_card_burner
%attr(755,root,root) %{_bindir}/usrp_n2xx_simple_net_burner
%attr(755,root,root) %{_bindir}/usrp_x3xx_fpga_burner
%{_mandir}/man1/octoclock_firmware_burner.1*
%{_mandir}/man1/uhd_cal_rx_iq_balance.1*
%{_mandir}/man1/uhd_cal_tx_dc_offset.1*
%{_mandir}/man1/uhd_cal_tx_iq_balance.1*
%{_mandir}/man1/uhd_find_devices.1*
%{_mandir}/man1/uhd_images_downloader.1*
%{_mandir}/man1/uhd_usrp_probe.1*
%{_mandir}/man1%{_prefix}p2_card_burner.1*
%{_mandir}/man1%{_prefix}p_n2xx_simple_net_burner.1*
%{_mandir}/man1%{_prefix}p_x3xx_fpga_burner.1*
%attr(755,root,root) %{_libdir}/libuhd.so.00*.00*
%attr(755,root,root) %ghost %{_libdir}/libuhd.so.003
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/utils
%attr(755,root,root) %{_libdir}/%{name}/utils/*.py
%{_libdir}/%{name}/utils/uhd-usrp.rules
%attr(755,root,root) %{_libdir}/%{name}/utils/*_eeprom
%attr(755,root,root) %{_libdir}/%{name}/utils/*_utils
%attr(755,root,root) %{_libdir}/%{name}/utils/*_sensors
%dir %{_libdir}/%{name}/utils/latency
%attr(755,root,root) %{_libdir}/%{name}/utils/latency/*

%files devel
%defattr(644,root,root,755)
%{_pkgconfigdir}/uhd.pc
%{_includedir}/uhd
%{_libdir}/cmake/uhd
%{_libdir}/libuhd.so

%files doc
%defattr(644,root,root,755)
%{_docdir}/%{name}
%dir %dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/examples
%attr(755,root,root) %{_libdir}/%{name}/examples/*
