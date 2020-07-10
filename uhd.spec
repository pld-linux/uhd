Summary:	Universal Hardware Driver for Ettus Research products
Summary(pl.UTF-8):	Uniwersalny sterownik sprzętowy do produktów Ettus Research
Name:		uhd
Version:	3.10.1.1
Release:	1
License:	GPL v3+
Group:		Applications/System
Source0:	https://files.ettus.com/binaries/uhd/src/%{name}-%{version}.tar.gz
# Source0-md5:	7b33dffef36c7c029104a49b0151b1ae
Patch0:		%{name}-boost.patch
Patch1:		%{name}-libdir.patch
URL:		https://www.ettus.com/sdr-software/uhd-usrp-hardware-driver/
BuildRequires:	boost-devel >= 1.53
BuildRequires:	cmake >= 2.8.0
BuildRequires:	doxygen
BuildRequires:	gpsd-devel >= 3.11
BuildRequires:	libstdc++-devel >= 6:4.8.0
BuildRequires:	libusb-devel >= 1.0
BuildRequires:	ncurses-devel
BuildRequires:	pkgconfig
BuildRequires:	python >= 1:2.7
BuildRequires:	python-Mako >= 0.4.2
BuildRequires:	python-requests >= 2.0
BuildRequires:	rpm-pythonprov
BuildRequires:	udev-devel
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The UHD is the universal hardware driver for Ettus Research products.
The goal of the UHD is to provide a host driver and API for current
and future Ettus Research products. It can be used standalone without
GNU Radio.

%description -l pl.UTF-8
UHD to uniwersalny sterownik sprzętowy do produktów Ettus Research.
Celem UHD jest zapewnienie sterownika gospodarza oraz API do obecnych
i przyszłych produków Ettus Research. Może być używany samodzielnie
bez GNU Radio.

%package libs
Summary:	USRP Hardware Driver library
Summary(pl.UTF-8):	Biblioteka USRP Hardware Driver
Group:		Libraries

%description libs
USRP Hardware Driver library.

%description libs -l pl.UTF-8
Biblioteka USRP Hardware Driver.

%package devel
Summary:	Development files for USRP Hardware Driver library
Summary(pl.UTF-8):	Pliki programistyczne biblioteki USRP Hardware Driver
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	boost-devel >= 1.53

%description devel
Header files for USRP Hardware Driver for Ettus Research products.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki USRP Hardware Driver (sterownika dla
sprzętu USRP) do produktów Ettus Research.

%package examples
Summary:	Examples for UHD
Summary(pl.UTF-8):	Przykłady do UHD
Group:		Applications/System
Requires:	%{name}-libs = %{version}-%{release}

%description examples
Example programs for USRP Hardware Driver for Ettus Research products.

%description examples -l pl.UTF-8
Programy przykładowe do biblioteki USRP Hardware Driver (sterownika
dla sprzętu USRP) do produktów Ettus Research.

%package doc
Summary:	Documentation for UHD
Summary(pl.UTF-8):	Dokumentacja do UHD
Group:		Documentation
%if "%{_rpmversion}" >= "4.6"
BuildArch:	noarch
%endif

%description doc
Documentation for USRP Hardware Driver for Ettus Research products.

%description doc -l pl.UTF-8
Dokumentacja do biblioteki USRP Hardware Driver (sterownika dla
sprzętu USRP) do produktów Ettus Research.

%prep
%setup -q -n UHD_%{version}_release
%patch0 -p1
%patch1 -p1

%{__sed} -i -e '1s,/usr/bin/env python$,%{__python},' utils/{converter_benchmark.py,uhd_images_downloader.py.in,usrp2_{card_burner,card_burner_gui,recovery}.py,usrp_n2xx_net_burner{,_gui}.py}
%{__sed} -i -e '1s,/usr/bin/env python$,%{__python},' utils/latency/graph.py

%build
install -d build
cd build
%cmake .. \
	-DENABLE_USB=ON

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{name}/utils/usrp_n2xx_simple_net_burner
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{name}/utils/usrp_x3xx_fpga_burner
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{name}/utils/latency/run_tests.py

# packaged as %doc
%{__rm} $RPM_BUILD_ROOT%{_docdir}/uhd/{LICENSE,README.md}

# not packaged
%{__rm} -r $RPM_BUILD_ROOT%{_libdir}/%{name}/tests

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE README.md
%attr(755,root,root) %{_bindir}/octoclock_firmware_burner
%attr(755,root,root) %{_bindir}/uhd_cal_rx_iq_balance
%attr(755,root,root) %{_bindir}/uhd_cal_tx_dc_offset
%attr(755,root,root) %{_bindir}/uhd_cal_tx_iq_balance
%attr(755,root,root) %{_bindir}/uhd_config_info
%attr(755,root,root) %{_bindir}/uhd_find_devices
%attr(755,root,root) %{_bindir}/uhd_image_loader
%attr(755,root,root) %{_bindir}/uhd_images_downloader
%attr(755,root,root) %{_bindir}/uhd_usrp_probe
%attr(755,root,root) %{_bindir}/usrp2_card_burner
%attr(755,root,root) %{_bindir}/usrp_n2xx_simple_net_burner
%attr(755,root,root) %{_bindir}/usrp_x3xx_fpga_burner
%{_mandir}/man1/octoclock_firmware_burner.1*
%{_mandir}/man1/uhd_cal_rx_iq_balance.1*
%{_mandir}/man1/uhd_cal_tx_dc_offset.1*
%{_mandir}/man1/uhd_cal_tx_iq_balance.1*
%{_mandir}/man1/uhd_config_info.1*
%{_mandir}/man1/uhd_find_devices.1*
%{_mandir}/man1/uhd_image_loader.1*
%{_mandir}/man1/uhd_images_downloader.1*
%{_mandir}/man1/uhd_usrp_probe.1*
%{_mandir}/man1/usrp2_card_burner.1*
%{_mandir}/man1/usrp_n2xx_simple_net_burner.1*
%{_mandir}/man1/usrp_x3xx_fpga_burner.1*
%dir %{_libdir}/%{name}/utils
%attr(755,root,root) %{_libdir}/%{name}/utils/b2xx_fx3_utils
%attr(755,root,root) %{_libdir}/%{name}/utils/converter_benchmark
%attr(755,root,root) %{_libdir}/%{name}/utils/converter_benchmark.py
%attr(755,root,root) %{_libdir}/%{name}/utils/fx2_init_eeprom
%attr(755,root,root) %{_libdir}/%{name}/utils/octoclock_burn_eeprom
%attr(755,root,root) %{_libdir}/%{name}/utils/query_gpsdo_sensors
%attr(755,root,root) %{_libdir}/%{name}/utils/uhd_images_downloader.py
%attr(755,root,root) %{_libdir}/%{name}/utils/usrp2_card_burner.py
%attr(755,root,root) %{_libdir}/%{name}/utils/usrp2_card_burner_gui.py
%attr(755,root,root) %{_libdir}/%{name}/utils/usrp2_recovery.py
%attr(755,root,root) %{_libdir}/%{name}/utils/usrp_burn_db_eeprom
%attr(755,root,root) %{_libdir}/%{name}/utils/usrp_burn_mb_eeprom
%attr(755,root,root) %{_libdir}/%{name}/utils/usrp_n2xx_net_burner.py
%attr(755,root,root) %{_libdir}/%{name}/utils/usrp_n2xx_net_burner_gui.py
%{_libdir}/%{name}/utils/uhd-usrp.rules
%dir %{_libdir}/%{name}/utils/latency
%attr(755,root,root) %{_libdir}/%{name}/utils/latency/graph.py
%attr(755,root,root) %{_libdir}/%{name}/utils/latency/responder
%{_datadir}/%{name}

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libuhd.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libuhd.so.003
%dir %{_libdir}/%{name}

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libuhd.so
%{_includedir}/uhd
%{_includedir}/uhd.h
%{_libdir}/cmake/uhd
%{_pkgconfigdir}/uhd.pc

%files examples
%defattr(644,root,root,755)
%dir %{_libdir}/%{name}/examples
%attr(755,root,root) %{_libdir}/%{name}/examples/*

%files doc
%defattr(644,root,root,755)
%{_docdir}/%{name}
