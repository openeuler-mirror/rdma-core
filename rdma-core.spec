Name:           rdma-core
Version:        35.1
Release:        2
Summary:        RDMA core userspace libraries and daemons
License:        GPLv2 or BSD
Url:            https://github.com/linux-rdma/rdma-core
Source:         https://github.com/linux-rdma/rdma-core/releases/download/v%{version}/%{name}-%{version}.tar.gz
Patch0:         backport-fixbug-increase-maximum-number-of-cpus-rdma.patch
Patch1:         riscv-barriers.patch

BuildRequires:  binutils cmake >= 2.8.11 gcc libudev-devel pkgconfig pkgconfig(libnl-3.0)
BuildRequires:  pkgconfig(libnl-route-3.0) valgrind-devel systemd systemd-devel
BuildRequires:  python3-devel python3-Cython python3 python3-docutils perl-generators
BuildRequires:  ninja-build

Requires:       systemd pciutils

Provides:       ibacm infiniband-diags-compat infiniband-diags libibverbs libibverbs-utils iwpmd libibumad librdmacm librdmacm-utils srp_daemon
Obsoletes:      ibacm infiniband-diags-compat infiniband-diags libibverbs libibverbs-utils iwpmd libibumad librdmacm librdmacm-utils srp_daemon

Provides:       rdma = %{version}-%{release}
Obsoletes:      rdma < %{version}-%{release}
Provides:       perl(IBswcountlimits)
Provides:       libibmad = %{version}-%{release}
Obsoletes:      libibmad < %{version}-%{release}
Obsoletes:      openib-diags < 1.3
Provides:       libcxgb4 = %{version}-%{release}
Obsoletes:      libcxgb4 < %{version}-%{release}
Provides:       libefa = %{version}-%{release}
Obsoletes:      libefa < %{version}-%{release}
Provides:       libhfi1 = %{version}-%{release}
Obsoletes:      libhfi1 < %{version}-%{release}
Provides:       libi40iw = %{version}-%{release}
Obsoletes:      libi40iw < %{version}-%{release}
Provides:       libipathverbs = %{version}-%{release}
Obsoletes:      libipathverbs < %{version}-%{release}
Provides:       libmlx4 = %{version}-%{release}
Obsoletes:      libmlx4 < %{version}-%{release}
Provides:       libmlx5 = %{version}-%{release}
Obsoletes:      libmlx5 < %{version}-%{release}
Provides:       libmthca = %{version}-%{release}
Obsoletes:      libmthca < %{version}-%{release}
Provides:       libocrdma = %{version}-%{release}
Obsoletes:      libocrdma < %{version}-%{release}
Provides:       librxe = %{version}-%{release}
Obsoletes:      librxe < %{version}-%{release}
Obsoletes:      srptools <= 1.0.3
Provides:       srptools = %{version}-%{release}
Obsoletes:      openib-srptools <= 0.0.6

Conflicts:      infiniband-diags <= 1.6.7

%{?systemd_requires}

%define CMAKE_FLAGS -GNinja
%define make_jobs ninja-build -v %{?_smp_mflags}
%define cmake_install DESTDIR=%{buildroot} ninja-build install

%description
This is the userspace components for the Linux Kernel's drivers/infiniband subsystem.
Specifically this contains the userspace libraries for the following device nodes:

  - /dev/infiniband/uverbsX (libibverbs)
  - /dev/infiniband/rdma_cm (librdmacm)
  - /dev/infiniband/umadX (libibumad)

%package        devel
Summary:        RDMA core development libraries and headers
Requires:       %{name} = %{version}-%{release}
Provides:       libibverbs-devel = %{version}-%{release}
Obsoletes:      libibverbs-devel < %{version}-%{release}
Provides:       libibumad-devel = %{version}-%{release}
Obsoletes:      libibumad-devel < %{version}-%{release}
Provides:       librdmacm-devel = %{version}-%{release}
Obsoletes:      librdmacm-devel < %{version}-%{release}
Provides:       ibacm-devel = %{version}-%{release}
Obsoletes:      ibacm-devel < %{version}-%{release}
Provides:       infiniband-diags-devel = %{version}-%{release}
Obsoletes:      infiniband-diags-devel < %{version}-%{release}
Provides:       libibmad-devel = %{version}-%{release}
Obsoletes:      libibmad-devel < %{version}-%{release}

BuildRequires:  pkgconfig(libnl-3.0) pkgconfig(libnl-route-3.0)

%description    devel
RDMA core development libraries and headers.

%package -n python3-pyverbs
Summary: Python3 API over IB verbs
%{?python_provide:%python_provide python3-pyverbs}

%description -n python3-pyverbs
Pyverbs is a Cython-based Python API over libibverbs, providing an
easy, object-oriented access to IB verbs.

%package help
Summary: Documents for %{name}
Buildarch: noarch
Requires: man info
Provides: infiniband-diags-help = %{version}-%{release}
Obsoletes: infiniband-diags-help < %{version}-%{release}

%description help
Man pages and other related documents for %{name}.

%prep
%setup
%autosetup -v -p1

%build
%if 0%{?_rundir:1}
%else
%define _rundir /var/run
%endif

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
         -DCMAKE_INSTALL_PERLDIR:PATH=%{perl_vendorlib} \
         -DENABLE_IBDIAGS_COMPAT:BOOL=True \
         -DENABLE_STATIC=1 \
         %{EXTRA_CMAKE_FLAGS} \
         -DPYTHON_EXECUTABLE:PATH=%{__python3} \
         -DCMAKE_INSTALL_PYTHON_ARCH_LIB:PATH=%{python3_sitearch} \
         -DNO_PYVERBS=0
%make_jobs

%install
%cmake_install

mkdir -p %{buildroot}/%{_sysconfdir}/rdma

%global dracutlibdir %{_prefix}/lib/dracut
%global sysmodprobedir %{_prefix}/lib/modprobe.d
mkdir -p %{buildroot}%{_sysconfdir}/udev/rules.d
mkdir -p %{buildroot}%{_libexecdir}
mkdir -p %{buildroot}%{_udevrulesdir}
mkdir -p %{buildroot}%{dracutlibdir}/modules.d/05rdma
mkdir -p %{buildroot}%{sysmodprobedir}
install -D -m 0644 redhat/rdma.mlx4.conf %{buildroot}/%{_sysconfdir}/rdma/mlx4.conf
install -D -m 0755 redhat/rdma.modules-setup.sh %{buildroot}%{dracutlibdir}/modules.d/05rdma/module-setup.sh
install -D -m 0644 redhat/rdma.mlx4.sys.modprobe %{buildroot}%{sysmodprobedir}/libmlx4.conf
install -D -m 0755 redhat/rdma.mlx4-setup.sh %{buildroot}%{_libexecdir}/mlx4-setup.sh
rm -f %{buildroot}%{_sysconfdir}/rdma/modules/rdma.conf
install -D -m0644 redhat/rdma.conf %{buildroot}%{_sysconfdir}/rdma/modules/rdma.conf

bin/ib_acme -D . -O
install -D -m 0644 ibacm_opts.cfg %{buildroot}%{_sysconfdir}/rdma/

rm -rf %{buildroot}/%{_initrddir}/
rm -f %{buildroot}/%{_sbindir}/srp_daemon.sh

%ldconfig_scriptlets

%post
if [ -x /sbin/udevadm ];then
/sbin/udevadm trigger --subsystem-match=infiniband --action=change || true
/sbin/udevadm trigger --subsystem-match=net --action=change || true
/sbin/udevadm trigger --subsystem-match=infiniband_mad --action=change || true
fi
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
%config(noreplace) %{_sysconfdir}/rdma/*.conf
%config(noreplace) %{_sysconfdir}/rdma/modules/*.conf
%config(noreplace) %{_sysconfdir}/udev/rules.d/*
%config(noreplace) %{_sysconfdir}/modprobe.d/*.conf
%config(noreplace) %{_sysconfdir}/infiniband-diags/*
%config(noreplace) %{_sysconfdir}/libibverbs.d/*.driver
%config(noreplace) %{_sysconfdir}/rdma/ibacm_opts.cfg
%config(noreplace) %{_sysconfdir}/iwpmd.conf
%config(noreplace) %{_sysconfdir}/srp_daemon.conf
%{dracutlibdir}/modules.d/05rdma/module-setup.sh
%{_udevrulesdir}/../rdma_rename
%{_udevrulesdir}/*.rules
%{sysmodprobedir}/libmlx4.conf
%{perl_vendorlib}/IBswcountlimits.pm
%{_libexecdir}/mlx4-setup.sh
%{_libexecdir}/truescale-serdes.cmds
%{_libexecdir}/srp_daemon/start_on_all_ports
%{_sbindir}/*
%{_bindir}/*
%{_unitdir}/*
%{_libdir}/libibmad*.so.*
%{_libdir}/libibnetdisc*.so.*
%{_libdir}/libefa.so.*
%{_libdir}/libibverbs*.so.*
%{_libdir}/libibverbs/*.so
%{_libdir}/libmlx5.so.*
%{_libdir}/libmlx4.so.*
%{_libdir}/ibacm/*
%{_libdir}/libibumad*.so.*
%{_libdir}/librdmacm*.so.*
%{_libdir}/rsocket/*.so*


%files devel
%defattr(-,root,root)
%{_includedir}/infiniband/*
%{_includedir}/rdma/*
%{_libdir}/lib*.a
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc

%files -n python3-pyverbs
%defattr(-,root,root)
%{python3_sitearch}/pyverbs
%{_docdir}/%{name}-%{version}/tests/*.py

%files help
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
* Tue Dec 28 2021 lvxiaoqian <xiaoqian@nj.iscas.ac.cn> - 35.1-2
- Type: requirement
- ID: NA
- SUG: NA
- DESC: add riscv patch, patch url:http://fedora.riscv.rocks/koji/buildinfo?buildID=87543

* Thu Dec 09 2021 gaihuiying <gaihuiying1@huawei.com> - 35.1-1
- Type: requirement
- ID: NA
- SUG: NA
- DESC: update to 35.1

* Fri Jul 2 2021 liyangyang <liyangyang20@huawei.com> - 35.0-1
- Type: bugfix
- ID: NA
- SUG: NA
- DESC: update to 35.0

* Mon Apr 20 2020 majun <majun65@huawei.com> - 28.1-2
- Type: bugfix
- ID: NA
- SUG: NA
- DESC: fix install problem

* Sat Apr 18 2020 majun <majun65@huawei.com> - 28.1-1
- Type: bugfix
- ID: NA
- SUG: NA
- DESC: update to 28.1

* Thu Mar 19 2020 wangxiaopeng <wangxiaopeng7@huawei.com> - 20.1-7
- Type: bugfix
- ID: NA
- SUG: NA
- DESC: fix upgrate problem

* Fri Oct 11 2019 jiangchuangang <jiangchuangang@huawei.com> - 20.1-6
- Type: enhancement
- ID: NA
- SUG: NA
- DESC: remove pandoc from BuildRequires

* Sat Sep 21 2019 openEuler Buildteam <buildteam@openeuler.org> - 20.1-5
- Package init

