
%define	ver_major 3
%define	ver_minor 8
%define	ver_patch 3

%define	ver %(printf "%03d.%03d.%03d" %{ver_major} %{ver_minor} %{ver_patch})
%define	ver_ %(printf "%03d_%03d_%03d" %{ver_major} %{ver_minor} %{ver_patch})

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
BuildRequires:	cmake >= 2.8.0
BuildRequires:	qt4-build
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

%package        doc
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
	../
%{__make}

cd ../

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C build install/fast \
	DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/uhd/utils%{_prefix}p_n2xx_simple_net_burner
rm -f $RPM_BUILD_ROOT%{_libdir}/uhd/utils%{_prefix}p_x3xx_fpga_burner

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

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
%attr(755,root,root) %{_bindir}%{_prefix}p2_card_burner
%attr(755,root,root) %{_bindir}%{_prefix}p_n2xx_simple_net_burner
%attr(755,root,root) %{_bindir}%{_prefix}p_x3xx_fpga_burner
%attr(755,root,root) %{_libdir}/libuhd.so.*.*
%ghost %{_libdir}/libuhd.so.003
%dir %{_libdir}/uhd
%attr(755,root,root) %{_libdir}/uhd/utils
%{_mandir}/man1/*

%files devel
%defattr(644,root,root,755)
%{_pkgconfigdir}/uhd.pc
%{_libdir}/cmake/uhd
%{_includedir}/uhd
%{_libdir}/*.so

%files doc
%defattr(644,root,root,755)
%{_docdir}/uhd
%{_libdir}/uhd/examples/benchmark_rate
%{_libdir}/uhd/examples/fpgpio
%{_libdir}/uhd/examples/latency_test
%{_libdir}/uhd/examples/network_relay
%{_libdir}/uhd/examples/rx_ascii_art_dft
%{_libdir}/uhd/examples/rx_multi_samples
%{_libdir}/uhd/examples/rx_samples_to_file
%{_libdir}/uhd/examples/rx_samples_to_udp
%{_libdir}/uhd/examples/rx_timed_samples
%{_libdir}/uhd/examples/test_clock_synch
%{_libdir}/uhd/examples/test_dboard_coercion
%{_libdir}/uhd/examples/test_messages
%{_libdir}/uhd/examples/test_pps_input
%{_libdir}/uhd/examples/test_timed_commands
%{_libdir}/uhd/examples/transport_hammer
%{_libdir}/uhd/examples/tx_bursts
%{_libdir}/uhd/examples/tx_samples_from_file
%{_libdir}/uhd/examples/tx_timed_samples
%{_libdir}/uhd/examples/tx_waveforms
%{_libdir}/uhd/examples/txrx_loopback_to_file
