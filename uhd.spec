#
# Conditional build
%bcond_without	mpm	# Module Peripheral Manager (run on embedded devices)
%bcond_with	dpdk	# DPDK support
%bcond_with	tests	# build tests

Summary:	Universal Hardware Driver for Ettus Research products
Summary(pl.UTF-8):	Uniwersalny sterownik sprzętowy do produktów Ettus Research
Name:		uhd
Version:	4.7.0.0
Release:	1
License:	GPL v3+
Group:		Applications/System
#Source0Download: https://github.com/EttusResearch/uhd/releases
Source0:	https://github.com/EttusResearch/uhd/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	8bd35c962d47822e9e4fc8572e2d2845
Patch0:		gcc13.patch
Patch1:		%{name}-libdir.patch
Patch3:		%{name}-mpm-build.patch
Patch4:		boost-1.87.patch
URL:		https://www.ettus.com/sdr-software/uhd-usrp-hardware-driver/
BuildRequires:	boost-devel >= 1.66
BuildRequires:	cmake >= 3.8
BuildRequires:	doxygen
%if %{with dpdk}
BuildRequires:	dpdk-devel >= 18.11
BuildRequires:	dpdk-devel < 21.12
%endif
%ifnarch %arch_with_atomics64
BuildRequires:	libatomic-devel
%endif
BuildRequires:	libstdc++-devel >= 6:6.3
BuildRequires:	libusb-devel >= 1.0
BuildRequires:	ncurses-devel
BuildRequires:	pkgconfig
BuildRequires:	python3 >= 1:3.6
BuildRequires:	python3-Mako >= 0.4.2
BuildRequires:	python3-devel >= 1:3.6
BuildRequires:	python3-modules >= 1:3.6
BuildRequires:	python3-numpy-devel >= 1.11
BuildRequires:	python3-requests >= 2.0
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.025
%if %{with mpm}
BuildRequires:	udev-devel
%endif
Requires:	%{name}-libs = %{version}-%{release}
Requires:	python3-uhd = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# per_lcore__lcore_id, per_lcore__rte_errno non-function symbols from dpdk
%define		skip_post_check_so	libuhd.so.*

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
Requires:	boost-devel >= 1.66

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
BuildArch:	noarch

%description doc
Documentation for USRP Hardware Driver for Ettus Research products.

%description doc -l pl.UTF-8
Dokumentacja do biblioteki USRP Hardware Driver (sterownika dla
sprzętu USRP) do produktów Ettus Research.

%package -n python3-uhd
Summary:	Python interface for USRP Hardware Driver library
Summary(pl.UTF-8):	Interfejs Pythona do biblioteki USRP Hardware Driver
Group:		Libraries/Python

%description -n python3-uhd
Python interface for USRP Hardware Driver library.

%description -n python3-uhd -l pl.UTF-8
Interfejs Pythona do biblioteki USRP Hardware Driver.

%package mpm
Summary:	USRP Module Peripheral Manager
Summary(pl.UTF-8):	USRP Module Peripheral Manager - zarządca urządzeń peryferyjnych
Group:		Applications/System
Requires:	%{name}-mpm-libs = %{version}-%{release}

%description mpm
USRP Module Peripheral Manager.

%description mpm -l pl.UTF-8
USRP Module Peripheral Manager - zarządca urządzeń peryferyjnych.

%package mpm-libs
Summary:	USRP Module Peripheral Manager library
Summary(pl.UTF-8):	Biblioteka USRP Module Peripheral Manager
Group:		Libraries

%description mpm-libs
USRP Module Peripheral Manager library.

%description mpm-libs -l pl.UTF-8
Biblioteka USRP Module Peripheral Manager.

%package mpm-devel
Summary:	USRP Module Peripheral Manager library
Summary(pl.UTF-8):	Biblioteka USRP Module Peripheral Manager
Group:		Development/Libraries
Requires:	%{name}-mpm-libs = %{version}-%{release}

%description mpm-devel
USRP Module Peripheral Manager library.

%description mpm-devel -l pl.UTF-8
Biblioteka USRP Module Peripheral Manager.

%package -n python3-usrp_mpm
Summary:	Python USRP Module Peripheral Manager library
Summary(pl.UTF-8):	Biblioteka USRP Module Peripheral Manager dla Pythona
Group:		Libraries/Python
Requires:	%{name}-mpm-libs = %{version}-%{release}

%description -n python3-usrp_mpm
Python USRP Module Peripheral Manager library.

%description -n python3-usrp_mpm -l pl.UTF-8
Biblioteka USRP Module Peripheral Manager dla Pythona.

%prep
%setup -q
%patch -P 0 -p1
%patch -P 1 -p1
%patch -P 3 -p1
%patch -P 4 -p1

%{__sed} -i -e '1s,/usr/bin/env python$,%{__python},' host/examples/python/*.py
%{__sed} -i -e '1s,/usr/bin/env python$,%{__python},' host/utils/{converter_benchmark.py,usrp2_{card_burner,card_burner_gui,recovery}.py}
%{__sed} -i -e '1s,/usr/bin/env python$,%{__python},' host/utils/latency/graph.py
grep -rl '/usr/bin/env python3' . | xargs %{__sed} -i -e '1s,/usr/bin/env python3,%{__python3},'

%build
install -d build-{host,mpm}
cd build-host
%cmake ../host \
	-DUHD_VERSION="%{version}" \
	%{!?with_dpdk:-DENABLE_DPDK=OFF} \
	%{cmake_on_off tests ENABLE_TESTS} \
	-DENABLE_USB=ON

%{__make}

%if %{with mpm}
cd ../build-mpm
%cmake ../mpm

# -DMPM_DEVICE= n3xx (Mykonos+Magnesium), e320, e31x
%endif

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build-host install \
	DESTDIR=$RPM_BUILD_ROOT

# outdated (binaries removed)
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man1/usrp_n2xx_simple_net_burner.1*
# not packaging tests
%{__rm}	$RPM_BUILD_ROOT%{_libdir}/%{name}/utils/latency/run_tests.py
%if %{with tests}
%{__rm} -r $RPM_BUILD_ROOT%{_libdir}/%{name}/tests
%endif
# packaged as %doc
%{__rm} $RPM_BUILD_ROOT%{_docdir}/uhd/{LICENSE,README.md}

%if %{with mpm}
%{__make} -C build-mpm install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_bindir}/aurora_bist_test.py

# combine all rules
LC_ALL=C sort -u mpm/systemd/udev/????/70-sfp-net.rules >$RPM_BUILD_ROOT/lib/udev/rules.d/70-sfp-net.rules

# configuration examples
%{__rm} $RPM_BUILD_ROOT/lib/systemd/network/{eth0,int0,sfp*}.network
%endif

%py3_comp $RPM_BUILD_ROOT%{py3_sitedir}
%py3_ocomp $RPM_BUILD_ROOT%{py3_sitedir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%post	mpm-libs -p /sbin/ldconfig
%postun	mpm-libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGELOG host/{LICENSE,README.md}
%attr(755,root,root) %{_bindir}/check-filesystem
%attr(755,root,root) %{_bindir}/rfnoc_image_builder
%attr(755,root,root) %{_bindir}/uhd_adc_self_cal
%attr(755,root,root) %{_bindir}/uhd_cal_rx_iq_balance
%attr(755,root,root) %{_bindir}/uhd_cal_tx_dc_offset
%attr(755,root,root) %{_bindir}/uhd_cal_tx_iq_balance
%attr(755,root,root) %{_bindir}/uhd_config_info
%attr(755,root,root) %{_bindir}/uhd_find_devices
%attr(755,root,root) %{_bindir}/uhd_image_loader
%attr(755,root,root) %{_bindir}/uhd_images_downloader
%attr(755,root,root) %{_bindir}/uhd_usrp_probe
%attr(755,root,root) %{_bindir}/usrp2_card_burner
%attr(755,root,root) %{_bindir}/usrpctl
%{_mandir}/man1/uhd_cal_rx_iq_balance.1*
%{_mandir}/man1/uhd_cal_tx_dc_offset.1*
%{_mandir}/man1/uhd_cal_tx_iq_balance.1*
%{_mandir}/man1/uhd_config_info.1*
%{_mandir}/man1/uhd_find_devices.1*
%{_mandir}/man1/uhd_image_loader.1*
%{_mandir}/man1/uhd_images_downloader.1*
%{_mandir}/man1/uhd_usrp_probe.1*
%{_mandir}/man1/usrp2_card_burner.1*
%{_mandir}/man1/usrpctl.1*
%dir %{_libdir}/%{name}/utils
%attr(755,root,root) %{_libdir}/%{name}/utils/b2xx_fx3_utils
%attr(755,root,root) %{_libdir}/%{name}/utils/convert_cal_data.py
%attr(755,root,root) %{_libdir}/%{name}/utils/converter_benchmark
%attr(755,root,root) %{_libdir}/%{name}/utils/converter_benchmark.py
%attr(755,root,root) %{_libdir}/%{name}/utils/fx2_init_eeprom
%attr(755,root,root) %{_libdir}/%{name}/utils/octoclock_burn_eeprom
%attr(755,root,root) %{_libdir}/%{name}/utils/query_gpsdo_sensors
%attr(755,root,root) %{_libdir}/%{name}/utils/uhd_images_downloader.py
%attr(755,root,root) %{_libdir}/%{name}/utils/uhd_power_cal.py
%attr(755,root,root) %{_libdir}/%{name}/utils/usrp2_card_burner.py
%attr(755,root,root) %{_libdir}/%{name}/utils/usrp2_recovery.py
%attr(755,root,root) %{_libdir}/%{name}/utils/usrp_burn_db_eeprom
%attr(755,root,root) %{_libdir}/%{name}/utils/usrp_burn_mb_eeprom
%{_libdir}/%{name}/utils/uhd-usrp.rules
%dir %{_libdir}/%{name}/utils/latency
%attr(755,root,root) %{_libdir}/%{name}/utils/latency/graph.py
%attr(755,root,root) %{_libdir}/%{name}/utils/latency/responder
%{_datadir}/%{name}

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libuhd.so.4.7.0
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

%files -n python3-uhd
%defattr(644,root,root,755)
%dir %{py3_sitedir}/uhd
%attr(755,root,root) %{py3_sitedir}/uhd/libpyuhd.cpython-*.so
%{py3_sitedir}/uhd/*.py
%{py3_sitedir}/uhd/__pycache__
%{py3_sitedir}/uhd/dsp
%{py3_sitedir}/uhd/imgbuilder
%{py3_sitedir}/uhd/usrp
%{py3_sitedir}/uhd/usrpctl
%{py3_sitedir}/uhd/utils

%if %{with mpm}
%files mpm
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/db-dump
%attr(755,root,root) %{_bindir}/db-id
%attr(755,root,root) %{_bindir}/db-init
%attr(755,root,root) %{_bindir}/eeprom-blank
%attr(755,root,root) %{_bindir}/eeprom-dump
%attr(755,root,root) %{_bindir}/eeprom-id
%attr(755,root,root) %{_bindir}/eeprom-init
%attr(755,root,root) %{_bindir}/eeprom-set-flags
%attr(755,root,root) %{_bindir}/fan-limits
%attr(755,root,root) %{_bindir}/mpm_debug.py
%attr(755,root,root) %{_bindir}/mpm_shell.py
%attr(755,root,root) %{_bindir}/n3xx_bist
%attr(755,root,root) %{_bindir}/usrp_hwd.py
%attr(755,root,root) %{_bindir}/usrp_update_fs
/lib/udev/rules.d/70-sfp-net.rules
%{systemdunitdir}/usrp-hwd.service
/usr/lib/sysctl.d/usrp-hwd.conf

%files mpm-libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libusrp-periphs.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libusrp-periphs.so.4

%files mpm-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libusrp-periphs.so
%{_includedir}/mpm

%files -n python3-usrp_mpm
%defattr(644,root,root,755)
%dir %{py3_sitedir}/usrp_mpm
%attr(755,root,root) %{py3_sitedir}/usrp_mpm/libpyusrp_periphs.so
%{py3_sitedir}/usrp_mpm/*.py
%{py3_sitedir}/usrp_mpm/__pycache__
%{py3_sitedir}/usrp_mpm/chips
%{py3_sitedir}/usrp_mpm/cores
%{py3_sitedir}/usrp_mpm/dboard_manager
%{py3_sitedir}/usrp_mpm/periph_manager
%{py3_sitedir}/usrp_mpm/sys_utils
%{py3_sitedir}/usrp_mpm/xports
%{py3_sitedir}/usrp_mpm/simulator
%endif
