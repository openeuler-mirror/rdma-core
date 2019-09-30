Name:		rdma-core
Version:	20.1
Release:	5
Summary:	RDMA core userspace libraries and daemons
License:	GPLv2 or BSD
URL:		https://github.com/linux-rdma/rdma-core
Source0:	https://github.com/linux-rdma/rdma-core/releases/download/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:	binutils cmake gcc libudev-devel pkgconfig libnl3-devel systemd
BuildRequires:  systemd-devel valgrind-devel pandoc python3 perl-generators make

Requires:	dracut kmod systemd

Provides:       rdma rdma-ndd libibverbs libcxgb3 libcxgb4 libhfi1 libi40iw libipathverbs 
Obsoletes:      rdma rdma-ndd libibverbs libcxgb3 libcxgb4 libhfi1 libi40iw libipathverbs libehca < 1.2.2-7
Provides:       libmlx4 libmlx5 libmthca libnes libocrdma librxe libusnic_verbs libibverbs-utils 
Obsoletes:      libmlx4 libmlx5 libmthca libnes libocrdma librxe libusnic_verbs libibverbs-utils 
Provides:       ibacm iwpmd libibumad librdmacm librdmacm-utils srp_daemon srptools
Obsoletes:      ibacm iwpmd libibumad librdmacm librdmacm-utils srp_daemon srptools openib-srptools <= 0.0.6

%{?systemd_requires}

%description
This is the userspace components for the Linux Kernel's drivers/infiniband subsystem. 
Specifically this contains the userspace libraries for the following device nodes:

  - /dev/infiniband/uverbsX (libibverbs)
  - /dev/infiniband/rdma_cm (librdmacm)
  - /dev/infiniband/umadX (libibumad)

%package        devel
Summary:        header files for rdma-core
Requires:       %{name} = %{version}-%{release}  
Provides:       libibverbs-devel libibverbs-devel-static libibumad-devel libibumad-static              
Obsoletes:      libibverbs-devel libibverbs-devel-static libibumad-devel libibumad-static 
Provides:       librdmacm-devel librdmacm-static ibacm-devel libcxgb3-static libcxgb4-static  
Obsoletes:      librdmacm-devel librdmacm-static ibacm-devel libcxgb3-static libcxgb4-static
Provides:       libhfi1-static libipathverbs-static libmlx4-static libmlx5-static libnes-static
Obsoletes:      libhfi1-static libipathverbs-static libmlx4-static libmlx5-static libnes-static
Provides:       libocrdma-static libi40iw-devel-static libmthca-static
Obsoletes:      libocrdma-static libi40iw-devel-static libmthca-static libibcm-devel 

%description    devel
Header files for rdma-core.

%package_help

%prep
%autosetup -n %{name}-%{version} -p1

%build
%if 0%{?_rundir:1}
%else
%define _rundir /var/run
%endif

%define make_jobs make -v %{?_smp_mflags}
%define cmake_install DESTDIR=%{buildroot} make install

%{!?EXTRA_CMAKE_FLAGS: %define EXTRA_CMAKE_FLAGS %{nil}}

%cmake %{CMAKE_FLAGS} \
         -DCMAKE_BUILD_TYPE=Release \
         -DCMAKE_INSTALL_BINDIR:PATH=%{_bindir} \
         -DCMAKE_INSTALL_SBINDIR:PATH=%{_sbindir} \
         -DCMAKE_INSTALL_LIBDIR:PATH=%{_libdir} \
         -DCMAKE_INSTALL_LIBEXECDIR:PATH=%{_libexecdir} \
         -DCMAKE_INSTALL_LOCALSTATEDIR:PATH=%{_localstatedir} \
         -DCMAKE_INSTALL_SHAREDSTATEDIR:PATH=%{_sharedstatedir} \
         -DCMAKE_INSTALL_INCLUDEDIR:PATH=%{_includedir} \
         -DCMAKE_INSTALL_INFODIR:PATH=%{_infodir} \
         -DCMAKE_INSTALL_MANDIR:PATH=%{_mandir} \
         -DCMAKE_INSTALL_SYSCONFDIR:PATH=%{_sysconfdir} \
         -DCMAKE_INSTALL_SYSTEMD_SERVICEDIR:PATH=%{_unitdir} \
         -DCMAKE_INSTALL_INITDDIR:PATH=%{_initrddir} \
         -DCMAKE_INSTALL_RUNDIR:PATH=%{_rundir} \
         -DCMAKE_INSTALL_DOCDIR:PATH=%{_docdir}/%{name}-%{version} \
         -DCMAKE_INSTALL_UDEV_RULESDIR:PATH=%{_udevrulesdir} \
         %{EXTRA_CMAKE_FLAGS} \
         .
%make_jobs

%install
%cmake_install

%global dracutlibdir %{_prefix}/lib/dracut
%global sysmodprobedir %{_prefix}/lib/modprobe.d

pushd redhat/
install -m 0644 rdma.conf %{buildroot}/%{_sysconfdir}/rdma/rdma.conf
install -m 0644 rdma.sriov-vfs %{buildroot}/%{_sysconfdir}/rdma/sriov-vfs
install -m 0644 rdma.mlx4.conf %{buildroot}/%{_sysconfdir}/rdma/mlx4.conf

install -m 0755 -d %{buildroot}%{sysmodprobedir}
install -m 0644 rdma.mlx4.sys.modprobe %{buildroot}/%{sysmodprobedir}/libmlx4.conf

install -m 0755 -d %{buildroot}%{_libexecdir}
install -m 0755 rdma.mlx4-setup.sh %{buildroot}/%{_libexecdir}/mlx4-setup.sh

install -m 0755 -d %{buildroot}%{_unitdir}
install -m 0644 rdma.service %{buildroot}%{_unitdir}/rdma.service

install -m 0755 -d %{buildroot}%{dracutlibdir}/modules.d/05rdma
install -m 0755 rdma.modules-setup.sh %{buildroot}%{dracutlibdir}/modules.d/05rdma/module-setup.sh

install -m 0755 -d %{buildroot}%{_udevrulesdir}
install -m 0644 rdma.udev-rules %{buildroot}%{_udevrulesdir}/98-rdma.rules

install -m 0755 -d %{buildroot}%{_libexecdir}
install -m 0755 rdma.kernel-init %{buildroot}%{_libexecdir}/rdma-init-kernel
install -m 0755 rdma.sriov-init %{buildroot}%{_libexecdir}/rdma-set-sriov-vf
popd

bin/ib_acme -D . -O
install -m 0644 ibacm_opts.cfg %{buildroot}%{_sysconfdir}/rdma/

%ldconfig_scriptlets 

%post
%systemd_post ibacm.service
%systemd_post srp_daemon.service
%systemd_post iwpmd.service

%preun
%systemd_preun ibacm.service
%systemd_preun srp_daemon.service	
%systemd_preun iwpmd.service

%postun
%systemd_postun_with_restart ibacm.service
%systemd_postun_with_restart srp_daemon.service
%systemd_postun_with_restart iwpmd.service

%files
%defattr(-,root,root)
%license COPYING.*
%{sysmodprobedir}/libmlx4.conf
%config(noreplace) %{_sysconfdir}/*.conf
%config(noreplace) %{_sysconfdir}/rdma/*.conf
%config(noreplace) %{_sysconfdir}/udev/rules.d/*
%config(noreplace) %{_sysconfdir}/rdma/sriov-vfs
%config(noreplace) %{_sysconfdir}/rdma/ibacm_opts.cfg
%config(noreplace) %{_sysconfdir}/rdma/modules/*.conf
%config(noreplace) %{_sysconfdir}/modprobe.d/*.conf
%config(noreplace) %{_sysconfdir}/libibverbs.d/*.driver
%{_libexecdir}/mlx4-setup.sh
%{dracutlibdir}/modules.d/05rdma/module-setup.sh
%{_sbindir}/*
%{_bindir}/*
%{_unitdir}/*
%{_udevrulesdir}/*.rules
%{_libexecdir}/rdma-init-kernel
%{_libexecdir}/rdma-set-sriov-vf
%{_libexecdir}/truescale-serdes.cmds
%{_libexecdir}/srp_daemon/start_on_all_ports
%{_libdir}/ibacm/*
%{_libdir}/libmlx4.so.*
%{_libdir}/libmlx5.so.*
%{_libdir}/libibverbs*.so.*
%{_libdir}/libibverbs/*.so
%{_libdir}/libibumad*.so.*
%{_libdir}/librdmacm*.so.*
%{_libdir}/rsocket/*.so*
%exclude %{_initrddir}/*
%exclude %{_sbindir}/srp_daemon.sh

%files       devel
%defattr(-,root,root)
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/rdma/*
%{_includedir}/infiniband/*

%files       help
%defattr(-,root,root)
%doc %{_docdir}/%{name}-%{version}/rxe.md
%doc %{_docdir}/%{name}-%{version}/udev.md
%doc %{_docdir}/%{name}-%{version}/ibacm.md
%doc %{_docdir}/%{name}-%{version}/README.md
%doc %{_docdir}/%{name}-%{version}/ibsrpdm.md
%doc %{_docdir}/%{name}-%{version}/MAINTAINERS
%doc %{_docdir}/%{name}-%{version}/librdmacm.md
%doc %{_docdir}/%{name}-%{version}/libibverbs.md
%doc %{_docdir}/%{name}-%{version}/tag_matching.md
%{_mandir}/*

%changelog
* Sat Sep 21 2019 openEuler Buildteam <buildteam@openeuler.org> - 20.1-5
- Package init
