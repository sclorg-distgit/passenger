%{?scl:%scl_package passenger}

%global bundled_boost_version 1.54.0
%global passenger_libdir %{_datadir}/passenger/
%global passenger_archdir %{_libdir}/passenger/
%global passenger_agentsdir %{_libexecdir}/passenger/

%define ruby200dir %{_builddir}/ruby200-%{name}-%{version}-%{release}
%define ruby22dir %{_builddir}/ruby22-%{name}-%{version}-%{release}
%global passenger_ruby200_archdir %{_libdir}/passenger200/
%global passenger_ruby22_archdir %{_libdir}/passenger22/
%global passenger_ruby193_archdir %{_libdir}/passenger193/

%if 0%{?scl:1}
%{!?_httpd24_apxs:       %{expand: %%global _httpd24_apxs       %%{_sbindir}/apxs}}
%{!?_httpd24_mmn:        %{expand: %%global _httpd24_mmn        %%(cat %{_includedir}/httpd/.mmn 2>/dev/null || echo missing-httpd-devel)}}
%{!?_httpd24_confdir:    %{expand: %%global _httpd24_confdir    %%{_sysconfdir}/httpd/conf.d}}
# /etc/httpd/conf.d with httpd < 2.4 and defined as /etc/httpd/conf.modules.d with httpd >= 2.4
%{!?_httpd24_modconfdir: %{expand: %%global _httpd24_modconfdir %%{_sysconfdir}/httpd/conf.d}}
%{!?_httpd24_moddir:    %{expand: %%global _httpd24_moddir    %%{_libdir}/httpd/modules}}
%else
%{!?_httpd_apxs:       %{expand: %%global _httpd_apxs       %%{_sbindir}/apxs}}
%{!?_httpd_mmn:        %{expand: %%global _httpd_mmn        %%(cat %{_includedir}/httpd/.mmn 2>/dev/null || echo missing-httpd-devel)}}
%{!?_httpd_confdir:    %{expand: %%global _httpd_confdir    %%{_sysconfdir}/httpd/conf.d}}
# /etc/httpd/conf.d with httpd < 2.4 and defined as /etc/httpd/conf.modules.d with httpd >= 2.4
%{!?_httpd_modconfdir: %{expand: %%global _httpd_modconfdir %%{_sysconfdir}/httpd/conf.d}}
%{!?_httpd_moddir:    %{expand: %%global _httpd_moddir    %%{_libdir}/httpd/modules}}
%endif

Summary: Phusion Passenger application server
Name: %{?scl:%scl_prefix}passenger
Version: 4.0.50
Release: 9%{?dist}
Group: System Environment/Daemons
# Passenger code uses MIT license.
# Bundled(Boost) uses Boost Software License
# BCrypt and Blowfish files use BSD license.
# Documentation is CC-BY-SA
# See: https://bugzilla.redhat.com/show_bug.cgi?id=470696#c146
License: Boost and BSD and BSD with advertising and MIT and zlib
URL: https://www.phusionpassenger.com

Source: http://s3.amazonaws.com/phusion-passenger/releases/passenger-%{version}.tar.gz
Source1: passenger.logrotate
Source2: rubygem-passenger.tmpfiles
Source10: apache-passenger.conf.in
Source12: config.json
# These scripts are needed only before we update httpd24-httpd.service
# in rhel7 to allow enabling extra SCLs.
Source13: passenger-ruby193
Source14: passenger-ruby200
Source15: passenger-ruby22
Source16: scl-register-helper.sh

# Load passenger_native_support.so from lib_dir
Patch0:           rubygem-passenger-4.0.18_native_dir.patch
# Use system libeio
Patch1:         passenger-4.0.38-libeio.patch
# ruby22 does not handle trap('KILL', 'DEFAULT')
Patch2:         passenger-4.0.50-kill-trap.patch
# Load daemon_controller using full path because of no other way how to
# change GEM_PATH while keeping the rh-passenger40 SCL ruby-agnostic.
Patch3:         passenger-4.0.50-standalone.patch
# httpd on RHEL7 is using private /tmp. This break passenger status.
# We workaround that by using "/var/run/passenger" instead of "/tmp".
Patch4:         passenger-4.0.50-tmpdir.patch
# Until rubygem-bluecloth is in Fedora, don't use it
Patch201:       rubygem-passenger-4.0.18-correct_docs.patch

BuildRequires: %{?scl:httpd24-}httpd-devel
BuildRequires: %{?scl:%scl_prefix}libev-devel >= 4.0.0
BuildRequires: %{?scl:ruby193-}ruby
BuildRequires: %{?scl:ruby193-}ruby-devel
BuildRequires: %{?scl:ruby193-}rubygems
BuildRequires: %{?scl:ruby193-}rubygems-devel
BuildRequires: %{?scl:ruby193-}rubygem(rake) >= 0.8.1
BuildRequires: %{?scl:ruby193-}rubygem(rack)
BuildRequires: %{?scl:ruby193-}rubygem(rspec)
BuildRequires: %{?scl:ruby193-}rubygem(mime-types)
BuildRequires: %{?scl:ruby193-}rubygem(sqlite3)
BuildRequires: %{?scl:%scl_prefix}rubygem(mizuho)

BuildRequires: %{?scl:ruby200-}ruby
BuildRequires: %{?scl:ruby200-}ruby-devel
BuildRequires: %{?scl:ruby200-}rubygems
BuildRequires: %{?scl:ruby200-}rubygems-devel
BuildRequires: %{?scl:ruby200-}rubygem(rake) >= 0.8.1
BuildRequires: %{?scl:ror40-}runtime
BuildRequires: %{?scl:ror40-}rubygem(rack)
BuildRequires: %{?scl:ror40-}rubygem(rspec)
BuildRequires: %{?scl:ror40-}rubygem(sqlite3)
BuildRequires: %{?scl:ror40-}rubygem(mime-types)

BuildRequires: %{?scl:rh-ruby22-}ruby
BuildRequires: %{?scl:rh-ruby22-}ruby-devel
BuildRequires: %{?scl:rh-ruby22-}rubygems
BuildRequires: %{?scl:rh-ruby22-}rubygems-devel
BuildRequires: %{?scl:rh-ruby22-}rubygem(rake) >= 0.8.1
BuildRequires: %{?scl:rh-ror41-}runtime
BuildRequires: %{?scl:rh-ror41-}rubygem(rack)
BuildRequires: %{?scl:rh-ror41-}rubygem(rspec)
BuildRequires: %{?scl:rh-ror41-}rubygem(sqlite3)
BuildRequires: %{?scl:rh-ror41-}rubygem(mime-types)

BuildRequires: libcurl-devel
# BuildRequires: source-highlight
BuildRequires: zlib-devel
BuildRequires: pcre-devel
BuildRequires: openssl-devel
BuildRequires: %{?scl:%scl_prefix}libeio-devel
%{?scl:Requires:%scl_runtime}
Requires: %{?scl:%scl_prefix}rubygem-daemon_controller
Requires(post): policycoreutils-python libselinux-utils

Provides: bundled(boost) = %{bundled_boost_version}

Conflicts: ruby193-rubygem-passenger40

# Suppress auto-provides for module DSO
%if 0%{?scl:1}
%{?filter_provides_in: %filter_provides_in %{_httpd24_moddir}/.*\.so$}
%else
%{?filter_provides_in: %filter_provides_in %{_httpd_moddir}/.*\.so$}
%endif
%{?filter_provides_in: %filter_provides_in %{passenger_ruby193_archdir}native/.*\.so$}
%{?filter_provides_in: %filter_provides_in %{passenger_ruby200_archdir}native/.*\.so$}
%{?filter_provides_in: %filter_provides_in %{passenger_ruby22_archdir}native/.*\.so$}
%{?filter_setup}

%description
Phusion Passenger® is a web server and application server, designed to be fast,
robust and lightweight. It takes a lot of complexity out of deploying web apps,
adds powerful enterprise-grade features that are useful in production,
and makes administration much easier and less complex. It supports Ruby,
Python, Node.js and Meteor.

%package -n %{scl_prefix}mod_passenger
Summary: Apache Module for Phusion Passenger
Group: System Environment/Daemons
BuildRequires:  httpd-devel
Requires: %{?scl:httpd24-}httpd-mmn = %{_httpd24_mmn}
Requires: %{name}%{?_isa} = %{version}-%{release}
Conflicts: ruby193-mod_passenger40
License: Boost and BSD and BSD with advertising and MIT and zlib

%description -n %{scl_prefix}mod_passenger
This package contains the pluggable Apache server module for Phusion Passenger®.

%package doc
Summary: Phusion Passenger documentation
Group: System Environment/Daemons
Requires: %{name} = %{version}-%{release}
BuildArch: noarch
License: CC-BY-SA and MIT and (MIT or GPL+)

%description doc
This package contains documentation files for Phusion Passenger®.

%package -n %{?scl:%scl_prefix}ruby193
Summary:   Phusion Passenger application server for ruby193
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: ruby193-ruby

%description -n %{?scl:%scl_prefix}ruby193
Phusion Passenger application server for ruby193.

%package -n %{?scl:%scl_prefix}ruby200
Summary:   Phusion Passenger application server for ruby200
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: ruby200-ruby

%description -n %{?scl:%scl_prefix}ruby200
Phusion Passenger application server for ruby200.

%package -n %{?scl:%scl_prefix}ruby22
Summary:   Phusion Passenger application server for rh-ruby22
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: rh-ruby22-ruby

%description -n %{?scl:%scl_prefix}ruby22
Phusion Passenger application server for rh-ruby22.

%prep
%setup -q %{?scl:-n %{pkg_name}-%{version}}

%patch0 -p1 -b .libdir
%patch1 -p1 -b .libeio
%patch2 -p1 -b .kill
%patch3 -p1 -b .standalone
%patch4 -p1 -b .tmpdir

# Until bluecloth is in Fedora, don't use it
%patch201 -p1 -b .docs

# Don't use bundled libev and libeio
rm -rf ext/libev
rm -rf ext/libeio

# Find files with a hash-bang that do not have executable permissions
for script in `find . -type f ! -perm /a+x -name "*.rb"`; do
    [ ! -z "`head -n 1 $script | grep \"^#!/\"`" ] && chmod -v 755 $script
done

rm -rf %{ruby200dir}
cp -a . %{ruby200dir}

rm -rf %{ruby22dir}
cp -a . %{ruby22dir}

%build

# Build the complete Passenger and shared module against ruby193.

%{?scl:scl enable ruby193 httpd24 rh-passenger40 - << \EOF}
export LD_LIBRARY_PATH=%{_libdir}:$LD_LIBRARY_PATH
export USE_VENDORED_LIBEV=false
export USE_VENDORED_LIBEIO=false
export GEM_PATH=%{gem_dir}:${GEM_PATH:+${GEM_PATH}}${GEM_PATH:-`scl enable ruby193 -- ruby -e "print Gem.path.join(':')"`}
CFLAGS="${CFLAGS:-%optflags}" ; export CFLAGS ;
CXXFLAGS="${CXXFLAGS:-%optflags}" ; export CXXFLAGS ;
EXTRA_CXX_LDFLAGS="-Wl,-rpath=%{_libdir},--enable-new-dtags "; export EXTRA_CXX_LDFLAGS;
FFLAGS="${FFLAGS:-%optflags}" ; export FFLAGS ;

export LANG=en_US.UTF-8
export LANGUAGE=en_US.UTF-8
export LC_ALL=en_US.UTF-8

rake fakeroot \
    NATIVE_PACKAGING_METHOD=rpm \
    FS_PREFIX=%{_prefix} \
    FS_BINDIR=%{_bindir} \
    FS_SBINDIR=%{_sbindir} \
    FS_DATADIR=%{_datadir} \
    FS_LIBDIR=%{_libdir} \
    FS_DOCDIR=%{_docdir} \
    RUBYLIBDIR=%{passenger_libdir} \
    RUBYARCHDIR=%{passenger_archdir} \
    APACHE2_MODULE_PATH=%{_httpd24_moddir}/mod_passenger.so 
%{?scl:EOF}

# Build just the shared module against ruby200

pushd %{ruby200dir}
%{?scl:scl enable ruby200 ror40 httpd24 rh-passenger40 - << \EOF}
export LD_LIBRARY_PATH=%{_libdir}:/opt/rh/ruby200/root/usr/lib64:/opt/rh/ruby193/root/usr/lib64:$LD_LIBRARY_PATH
export USE_VENDORED_LIBEV=false
export USE_VENDORED_LIBEIO=false
export GEM_PATH=%{gem_dir}:${GEM_PATH:+${GEM_PATH}}${GEM_PATH:-`scl enable ruby200 -- ruby -e "print Gem.path.join(':')"`}
CFLAGS="${CFLAGS:-%optflags}" ; export CFLAGS ;
CXXFLAGS="${CXXFLAGS:-%optflags}" ; export CXXFLAGS ;
FFLAGS="${FFLAGS:-%optflags}" ; export FFLAGS ;

export LANG=en_US.UTF-8
export LANGUAGE=en_US.UTF-8
export LC_ALL=en_US.UTF-8

rake fakeroot \
    NATIVE_PACKAGING_METHOD=rpm \
    FS_PREFIX=%{_prefix} \
    FS_BINDIR=%{_bindir} \
    FS_SBINDIR=%{_sbindir} \
    FS_DATADIR=%{_datadir} \
    FS_LIBDIR=%{_libdir} \
    FS_DOCDIR=%{_docdir} \
    RUBYLIBDIR=%{passenger_libdir} \
    RUBYARCHDIR=%{passenger_ruby200_archdir} \
    APACHE2_MODULE_PATH=%{_httpd24_moddir}/mod_passenger.so 
    ONLY_RUBY=1
%{?scl:EOF}
popd

# Build just the shared module against ruby22

pushd %{ruby22dir}
%{?scl:scl enable rh-ruby22 rh-ror41 httpd24 rh-passenger40 - << \EOF}
export LD_LIBRARY_PATH=%{_libdir}:/opt/rh/rh-ruby22/root/usr/lib64:/opt/rh/ruby193/root/usr/lib64:$LD_LIBRARY_PATH
export USE_VENDORED_LIBEV=false
export USE_VENDORED_LIBEIO=false
export GEM_PATH=%{gem_dir}:${GEM_PATH:+${GEM_PATH}}${GEM_PATH:-`scl enable rh-ruby22 -- ruby -e "print Gem.path.join(':')"`}
CFLAGS="${CFLAGS:-%optflags}" ; export CFLAGS ;
CXXFLAGS="${CXXFLAGS:-%optflags}" ; export CXXFLAGS ;
FFLAGS="${FFLAGS:-%optflags}" ; export FFLAGS ;

export LANG=en_US.UTF-8
export LANGUAGE=en_US.UTF-8
export LC_ALL=en_US.UTF-8

rake fakeroot \
    NATIVE_PACKAGING_METHOD=rpm \
    FS_PREFIX=%{_prefix} \
    FS_BINDIR=%{_bindir} \
    FS_SBINDIR=%{_sbindir} \
    FS_DATADIR=%{_datadir} \
    FS_LIBDIR=%{_libdir} \
    FS_DOCDIR=%{_docdir} \
    RUBYLIBDIR=%{passenger_libdir} \
    RUBYARCHDIR=%{passenger_ruby22_archdir} \
    APACHE2_MODULE_PATH=%{_httpd24_moddir}/mod_passenger.so 
    ONLY_RUBY=1
%{?scl:EOF}
popd

%install
%{?scl:scl enable ruby193 httpd24 rh-passenger40 - << \EOF}
#include helper script for creating register stuff
source %{SOURCE16}

# configure variables for the helper function scl_reggen
export _SR_BUILDROOT=%{buildroot}
export _SR_SCL_SCRIPTS=%{?_scl_scripts}

export USE_VENDORED_LIBEV=false
export USE_VENDORED_LIBEIO=false

export LANG=en_US.UTF-8
export LANGUAGE=en_US.UTF-8
export LC_ALL=en_US.UTF-8

cp -a pkg/fakeroot/* %{buildroot}/

# Install bootstrapping code into the executables and the Nginx config script.
./dev/install_scripts_bootstrap_code.rb --ruby %{passenger_libdir} %{buildroot}%{_bindir}/* %{buildroot}%{_sbindir}/*

# Install Apache module.
mkdir -p %{buildroot}/%{_httpd24_moddir}
install -pm 0755 buildout/apache2/mod_passenger.so %{buildroot}/%{_httpd24_moddir}

# Install Apache config.
mkdir -p %{buildroot}%{_httpd24_confdir} %{buildroot}%{_httpd24_modconfdir}
sed -e 's|@PASSENGERROOT@|%{passenger_libdir}/phusion_passenger/locations.ini|g' %{SOURCE10} > passenger.conf
sed -i 's|@PASSENGERRUBY@|%{_libexecdir}/passenger-ruby193|g' passenger.conf

%if "%{_httpd24_modconfdir}" != "%{_httpd24_confdir}"
    sed -n /^LoadModule/p passenger.conf > 10-passenger.conf
    sed -i /^LoadModule/d passenger.conf
    touch -r %{SOURCE10} 10-passenger.conf
    install -pm 0644 10-passenger.conf %{buildroot}%{_httpd24_modconfdir}/passenger.conf
%endif
touch -r %{SOURCE10} passenger.conf
install -pm 0644 passenger.conf %{buildroot}%{_httpd24_confdir}/passenger.conf

# Install wrappers to allow using multiple Ruby versions in single httpd
# instance.
%{__mkdir_p} %{buildroot}%{_libexecdir}/
install -pm 0755 %{SOURCE13} %{buildroot}%{_libexecdir}/passenger-ruby193
install -pm 0755 %{SOURCE14} %{buildroot}%{_libexecdir}/passenger-ruby200
install -pm 0755 %{SOURCE15} %{buildroot}%{_libexecdir}/passenger-ruby22

# Move agents to libexec
mkdir -p %{buildroot}/%{passenger_agentsdir}
mv %{buildroot}/%{passenger_archdir}/agents/* %{buildroot}/%{passenger_agentsdir}
rm -d %{buildroot}/%{passenger_archdir}/agents/
sed -i 's|%{passenger_archdir}agents|%{passenger_agentsdir}|g' \
    %{buildroot}%{passenger_libdir}/phusion_passenger/locations.ini

# Make our ghost log and run directories...
# mkdir -p %{buildroot}%{_root_localstatedir}/log/passenger-analytics

# logrotate
# mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d
# install -pm 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/logrotate.d/passenger

# tmpfiles.d
%if 0%{?rhel} > 6
    mkdir -p %{buildroot}%{_root_localstatedir}/run
    mkdir -p %{buildroot}%{_root_prefix}/lib/tmpfiles.d
    install -m 0644 %{SOURCE2} %{buildroot}%{_root_prefix}/lib/tmpfiles.d/rh-passenger40.conf
    install -d -m 0755 %{buildroot}%{_root_localstatedir}/run/rh-passenger40

    scl_reggen %{name} --mkdir %{_root_localstatedir}/run/rh-passenger40
    scl_reggen %{name} --chmod %{_root_localstatedir}/run/rh-passenger40 0755
    scl_reggen %{name} --cpfile %{_root_prefix}/lib/tmpfiles.d/rh-passenger40.conf
%else
    mkdir -p %{buildroot}%{_root_localstatedir}/run/rh-passenger40
    scl_reggen %{name} --mkdir %{_root_localstatedir}/run/rh-passenger40
%endif

# Install man pages into the proper location.
mkdir -p %{buildroot}%{_mandir}/man1
mkdir -p %{buildroot}%{_mandir}/man8
cp man/*.1 %{buildroot}%{_mandir}/man1
cp man/*.8 %{buildroot}%{_mandir}/man8

# Fix Python scripts with shebang which are not executable
chmod +x %{buildroot}%{_datadir}/passenger/helper-scripts/wsgi-loader.py

# Remove empty release.txt file
rm -f %{buildroot}%{_datadir}/passenger/release.txt

# Remove object files and source files. They are needed to compile nginx
# using "passenger-install-nginx-module", but it's not according to
# guidelines. Debian does not provide these files too, so we stay consistent.
# In the long term, it would be better to allow Fedora nginx to support
# Passenger.
rm -rf %{buildroot}%{passenger_libdir}/ngx_http_passenger_module
rm -rf %{buildroot}%{passenger_libdir}/ruby_extension_source
rm -rf %{buildroot}%{passenger_libdir}/include
rm -rf %{buildroot}%{_libdir}/passenger/common
rm -rf %{buildroot}%{_bindir}/passenger-install-*-module

# Fix shebang
sed -i 's|/opt/rh/rh-passenger40/root/usr/bin/ruby|/usr/bin/env ruby|g' \
    %{buildroot}%{_sbindir}/passenger-status
sed -i 's|/opt/rh/rh-passenger40/root/usr/bin/ruby|/usr/bin/env ruby|g' \
    %{buildroot}%{_sbindir}/passenger-memory-stats

# Install ruby193 shared module
mkdir -p %{buildroot}/%{passenger_ruby193_archdir}/native
mv %{buildroot}/%{passenger_archdir}/*.so %{buildroot}/%{passenger_ruby193_archdir}/native
rm -rf %{buildroot}/%{passenger_archdir}

# Install ruby200 shared module
pushd %{ruby200dir}
mkdir -p %{buildroot}/%{passenger_ruby200_archdir}/native
cp -a buildout/ruby/*/passenger_native_support.so %{buildroot}/%{passenger_ruby200_archdir}/native
popd

# Install ruby22 shared module
pushd %{ruby22dir}
mkdir -p %{buildroot}/%{passenger_ruby22_archdir}/native
cp -a buildout/ruby/*/passenger_native_support.so %{buildroot}/%{passenger_ruby22_archdir}/native
popd

# Link PassengerWebHelper to nginx16 SCL
ln -s /opt/rh/nginx16/root/usr/sbin/nginx %{buildroot}%{passenger_agentsdir}PassengerWebHelper

%{?scl:EOF}

%post
semanage fcontext -a -t passenger_exec_t "%{_root_libexecdir}/passenger/PassengerHelperAgent"
semanage fcontext -a -t passenger_exec_t "%{_root_libexecdir}/passenger/PassengerLoggingAgent"
semanage fcontext -a -t passenger_exec_t "%{_root_libexecdir}/passenger/PassengerWatchdog"
semanage fcontext -a -t passenger_exec_t "%{_root_libexecdir}/passenger/SpawnPreparer"
semanage fcontext -a -t passenger_exec_t "%{_root_libexecdir}/passenger/TempDirToucher"
restorecon -R %{_scl_root} >/dev/null 2>&1 || :

%check
%{?scl:scl enable ruby193 httpd24 rh-passenger40 - << \EOF}
export USE_VENDORED_LIBEV=false
export USE_VENDORED_LIBEIO=false

# Running the full test suite is not only slow, but also impossible
# because not all requirements are packaged by Fedora. It's also not
# too useful because Phusion Passenger is automatically tested by a CI
# server on every commit. The C++ tests are the most likely to catch
# any platform-specific bugs (e.g. bugs caused by wrong compiler options)
# so we only run those. Note that the C++ tests are highly timing
# sensitive, so sometimes they may fail even though nothing is really
# wrong. We therefore do not make failures fatal, although the result
# should still be checked.
# Currently the tests fail quite often on ARM because of the slower machines.
cp %{SOURCE12} test/config.json
rake test:cxx || true
%{?scl:EOF}

%files
%doc LICENSE CONTRIBUTORS CHANGELOG
%{_bindir}/passenger*
%if 0%{?rhel} > 6
%{_root_prefix}/lib/tmpfiles.d/rh-passenger40.conf
%{?scl: %{_scl_scripts}/register.content/*}
%endif
%dir %{_root_localstatedir}/run/rh-passenger40
# %dir %{_localstatedir}/log/passenger-analytics
# %config(noreplace) %{_sysconfdir}/logrotate.d/passenger
%{passenger_libdir}
%{passenger_agentsdir}
%{_sbindir}/*
%{_mandir}/man1/*
%{_mandir}/man8/*
%{?scl: %{_scl_scripts}/register.d/*}
%{?scl: %{_scl_scripts}/deregister.d/*}

%files -n %{?scl:%scl_prefix}ruby193
%doc LICENSE CONTRIBUTORS CHANGELOG
%{passenger_ruby193_archdir}
%{_libexecdir}/passenger-ruby193

%files -n %{?scl:%scl_prefix}ruby200
%doc LICENSE CONTRIBUTORS CHANGELOG
%{passenger_ruby200_archdir}
%{_libexecdir}/passenger-ruby200

%files -n %{?scl:%scl_prefix}ruby22
%doc LICENSE CONTRIBUTORS CHANGELOG
%{passenger_ruby22_archdir}
%{_libexecdir}/passenger-ruby22

%files doc
%doc %{_docdir}/passenger

%files -n %{scl_prefix}mod_passenger
%config(noreplace) %{_httpd24_modconfdir}/*.conf
%if "%{_httpd24_modconfdir}" != "%{_httpd24_confdir}"
%config(noreplace) %{_httpd24_confdir}/*.conf
%endif
%doc doc/Users?guide?Apache.txt
%{_httpd24_moddir}/mod_passenger.so


%changelog
* Fri Mar 13 2015 Jan Kaluza <jkaluza@redhat.com> - 4.0.50-9
- filter out private libraries from Provides (#1201501)

* Wed Jan 28 2015 Jan Kaluza <jkaluza@redhat.com> - 4.0.50-8
- add conflicts with ruby193-rubygem-passenger40 packages (#1186723)

* Thu Jan 22 2015 Jan Kaluza <jkaluza@redhat.com> - 4.0.50-7
- set proper selinux context to agents
- add support for "scl register"

* Thu Jan 22 2015 Jan Kaluza <jkaluza@redhat.com> - 4.0.50-6
- rebuild against new libev and libeio

* Wed Jan 21 2015 Jan Kaluza <jkaluza@redhat.com> - 4.0.50-5
- use /var/run/passenger instead of /tmp for temporary directory
- use rpath to find libev and libev-eio

* Tue Jan 20 2015 Jan Kaluza <jkaluza@redhat.com> - 4.0.50-4
- rename httpd24-ruby* wrappers to passenger-ruby*
- support "passenger start" with nginx16 SCL

* Mon Jan 19 2015 Jan Kaluza <jkaluza@redhat.com> - 4.0.50-3
- add support for rh-ruby22

* Thu Jan 08 2015 Jan Kaluza <jkaluza@redhat.com> - 4.0.50-2
- allow enabling additional SCLs using service-environment

* Tue Sep 09 2014 Jan Kaluza <jkaluza@redhat.com> - 4.0.50-1
- update to new upstream version 4.0.50

* Tue Sep 09 2014 Jan Kaluza <jkaluza@redhat.com> - 4.0.41-2
- add support for rhel7

* Tue May 27 2014 Jan Kaluza <jkaluza@redhat.com> - 4.0.41-1
- update to version 4.0.41

* Tue May 13 2014 Jan Kaluza <jkaluza@redhat.com> - 4.0.38-1
- renamed from rubygem-passenger to passenger
- changed the packaging structure to be closer to upstream
- update to 4.0.38 (#1060106)
- fix for CVE-2014-1831 and CVE-2014-1832
- use real commands without macros
- do not bundle libeio

* Thu Jan 23 2014 Joe Orton <jorton@redhat.com> - 4.0.18-5
- fix _httpd_mmn expansion in absence of httpd-devel

* Thu Nov 14 2013 Jan Kaluza <jkaluza@redhat.com> - 4.0.18-4
- load native library from proper path

* Thu Oct 31 2013 Jan Kaluza <jkaluza@redhat.com> - 4.0.18-3
- fix #1021940 - add locations.ini with proper Fedora locations

* Wed Sep 25 2013 Troy Dawson <tdawson@redhat.com> - 4.0.18-2
- Cleanup spec file
- Fix for bz#987879

* Tue Sep 24 2013 Troy Dawson <tdawson@redhat.com> - 4.0.18-1
- Update to 4.0.18
- Remove patches no longer needed
- Update patches that need updating

* Mon Sep 23 2013 Brett Lentz <blentz@redhat.com> - 3.0.21-9
- finish fixing bz#999384

* Fri Sep 20 2013 Joe Orton <jorton@redhat.com> - 3.0.21-8
- update packaging for httpd 2.4.x

* Thu Sep 19 2013 Troy Dawson <tdawson@redhat.com> - 3.0.21-7
- Fix for F20 FTBFS (#993310)

* Thu Aug 22 2013 Brett Lentz <blentz@redhat.com> - 3.0.21-6
- bz#999384

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.21-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Troy Dawson <tdawson@redhat.com> - 3.0.21-4
- Fix for CVE-2013-4136 (#985634)

* Fri Jun 21 2013 Troy Dawson <tdawson@redhat.com> - 3.0.21-3
- Putting the agents back to where they originally were

* Fri Jun 21 2013 Troy Dawson <tdawson@redhat.com> - 3.0.21-2
- Remove Rakefile (only used for building) (#976843)

* Thu May 30 2013 Troy Dawson <tdawson@redhat.com> - 3.0.21-1
- Update to version 3.0.21
- Fix for CVE-2013-2119

* Thu May 16 2013 Troy Dawson <tdawson@redhat.com> - 3.0.19-4
- Fix to make agents work on F19+

* Wed Mar 13 2013 Troy Dawson <tdawson@redhat.com> - 3.0.19-3
- Fix to make it build/install on F19+
- Added patch105

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jan 20 2013 Orion Poplawski <orion@cora.nwra.com> - 3.0.19-1
- Update to 3.0.19

* Wed Sep 19 2012 Orion Poplawski <orion@cora.nwra.com> - 3.0.17-3
- Drop dependency on rubygem(file-tail), no longer needed

* Fri Sep 7 2012 Brett Lentz <blentz@redhat.com> - 3.0.17-2
- Fix License

* Thu Sep 6 2012 Brett Lentz <blentz@redhat.com> - 3.0.17-1
- update to 3.0.17

* Wed Sep 5 2012 Brett Lentz <blentz@redhat.com> - 3.0.14-15
- add support for tmpfiles.d

* Tue Sep 4 2012 Brett Lentz <blentz@redhat.com> - 3.0.14-14
- Fix License tag
- Fix gem_extdir ownership issue

* Wed Aug 29 2012 Brett Lentz <blentz@redhat.com> - 3.0.14-13
- fix pathing issues
- fix ruby abi requires

* Wed Aug 29 2012 Brett Lentz <blentz@redhat.com> - 3.0.14-12
- remove capability for running passenger standalone until daemon_controller is updated

* Tue Aug 28 2012 Brett Lentz <blentz@redhat.com> - 3.0.14-11
- fix issues with fastthread

* Mon Aug 27 2012 Brett Lentz <blentz@redhat.com> - 3.0.14-10
- get test suite sort of working
- move agents to gem_extdir

* Fri Aug 24 2012 Brett Lentz <blentz@redhat.com> - 3.0.14-9
- stop using _bindir
- fix native libs path
- fix ownership on extdir
- improve test output

* Wed Aug 22 2012 Brett Lentz <blentz@redhat.com> - 3.0.14-8
- removed policycoreutils requirement
- moved native libs to gem_extdir

* Wed Aug 22 2012 Brett Lentz <blentz@redhat.com> - 3.0.14-7
- remove selinux policy module. it's in the base policy now.

* Fri Aug 17 2012 Brett Lentz <blentz@redhat.com> - 3.0.14-6
- put native-libs into ruby_vendorarchdir.

* Thu Aug 16 2012 Brett Lentz <blentz@redhat.com> - 3.0.14-5
- clean up packaging and file placement.
- add logrotate file for /var/log/passenger-analytics

* Wed Aug 15 2012 Brett Lentz <blentz@redhat.com> - 3.0.14-4
- backported fix only needed on f18+

* Wed Aug 15 2012 Brett Lentz <blentz@redhat.com> - 3.0.14-3
- backport fix from https://svn.boost.org/trac/boost/ticket/6940

* Mon Aug 13 2012 Brett Lentz <blentz@redhat.com> - 3.0.14-2
- remove F15 conditional. F15 is EOL.

* Fri Jul 27 2012 Troy Dawson <tdawson@redhat.com> - 3.0.14-1
- Updated to version 3.0.14

* Fri Jul 27 2012 Troy Dawson <tdawson@redhat.com> - 3.0.12-6
- Added patch20, spawn-ip
- Changed selinux files to be more dynamic

* Tue Jun 05 2012 Troy Dawson <tdawson@redhat.com> - 3.0.12-5
- Add all the selinux files

* Tue Jun 05 2012 Troy Dawson <tdawson@redhat.com> - 3.0.12-4
- Added selinux configurations

* Tue Jun 05 2012 Troy Dawson <tdawson@redhat.com> - 3.0.12-3
- Added native and native-libs rpms.

* Mon Apr 16 2012 Brett Lentz <blentz@redhat.com> - 3.0.12-2
- Add dist to release.
- Shuffle around deprecated buildrequires and requires.

* Mon Apr 16 2012 Brett Lentz <blentz@redhat.com> - 3.0.12-1
- Update to 3.0.12
- Incorporate specfile changes from kanarip's version

* Wed Apr 11 2012 Brett Lentz <blentz@redhat.com> - 3.0.11-1
- Initial spec file
