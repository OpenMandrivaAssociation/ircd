%define name ircd
%define version 2.11.1
%define patchlevel 1
%if %patchlevel
  %define distname irc%{version}p%{patchlevel}
  %define rel p%{patchlevel}.1
%else
  %define distname %{name}%{version}
%define rel 1
%endif
%define release %mkrel %{rel}

Name:		%{name}
Summary:	IRC server from ftp.irc.org
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Networking/IRC
URl: 		http://www.irc.org/
Source0:	ftp://ftp.irc.org/irc/server/%{distname}.tar.bz2
Source1:	ircd.init
Source2:	README.urpmi
Source3:	ircd_crypter
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	zlib-devel
Requires(pre):	rpm-helper
Requires(post):	rpm-helper

%description
ircd is the server (daemon) program for the Internet Relay Chat Program. The 
ircd is a server in that its function is to "serve" the client program irc(1) 
with messages and commands. All commands and user messages are passed directly 
to the ircd for processing and relaying to other ircd sites.

%prep
%setup -q -n %{distname}

%build
%configure2_5x \
	--localstatedir=/var/run \
	--sysconfdir=%{_sysconfdir}/ircd
%make -C `support/config.guess` server

%install
rm -rf $RPM_BUILD_ROOT
%make install -C `support/config.guess` \
	server_bin_dir=$RPM_BUILD_ROOT%{_sbindir} \
	conf_man_dir=$RPM_BUILD_ROOT%{_mandir}/man5 \
	server_man_dir=$RPM_BUILD_ROOT%{_mandir}/man8 \
	ircd_conf_dir=$RPM_BUILD_ROOT%{_sysconfdir}/%{name} \
	ircd_var_dir=$RPM_BUILD_ROOT/var/run \
	ircd_log_dir=$RPM_BUILD_ROOT/var/log \
	install-server

install -m 711 %{SOURCE3} $RPM_BUILD_ROOT%{_sbindir}/ircd-crypter

install -d $RPM_BUILD_ROOT%{_initrddir}
install -m 750 %{SOURCE1} $RPM_BUILD_ROOT%{_initrddir}/%{name}

install -m 644 %{SOURCE1} doc/README.update.urpmi

%post
%_post_service %{name}
touch /var/log/auth
touch /var/log/opers
touch /var/log/rejects
touch /var/log/users
# update /etc/ircd/ircd.m4
DOMAIN=`egrep '^domain' /etc/resolv.conf | \
	sed -e 's/^domain[     ]*\([^   ]*\).*/\1/'`
HOST=`hostname | sed -e 's/\([a-zA-Z0-9\-]*\).*/\1/'`
sed "s/define(HOSTNAME,.*)/define(HOSTNAME,$HOST)/g" /etc/ircd/ircd.m4 >/etc/ircd/ircd.m4.new
sed "s/define(DOMAIN,.*)/define(DOMAIN,$DOMAIN)/g" /etc/ircd/ircd.m4.new >/etc/ircd/ircd.m4
rm -f /etc/ircd/ircd.m4.new


%preun
%_preun_service %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc doc/2.* doc/Authors doc/BUGS doc/ChangeLog doc/Etiquette doc/INSTALL.*
%doc doc/LICENSE doc/README doc/RELEASE* doc/SERVICE* doc/alt-irc-faq
%doc doc/iauth-internals.txt doc/m4macros
%doc doc/Juped doc/Nets doc/ISO-3166-1
%doc doc/README.update.urpmi
%{_sbindir}/*
%{_mandir}/man8/ircd.8.*
%{_mandir}/man8/iauth.8.*
%{_mandir}/man8/ircdwatch.8.*
%{_mandir}/man5/iauth.conf.5.*
%config(noreplace) %{_sysconfdir}/ircd/ircd.m4
%config(noreplace) %{_sysconfdir}/ircd/ircd.motd
%config(noreplace) %{_sysconfdir}/ircd/iauth.conf
%config(noreplace) %{_sysconfdir}/ircd/iauth.conf.example
%config(noreplace) %{_sysconfdir}/ircd/ircd.conf.example
%{_initrddir}/%{name}


