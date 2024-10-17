%define name ircd
%define version 2.11.1
%define patchlevel 1
%if %patchlevel
  %define distname irc%{version}p%{patchlevel}
  %define rel p%{patchlevel}.2
%else
  %define distname %{name}%{version}
%define rel 3
%endif
%define release %mkrel %{rel}

Name:		%{name}
Summary:	IRC server from ftp.irc.org
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Networking/IRC
URl: 		https://www.irc.org/
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




%changelog
* Fri Dec 10 2010 Oden Eriksson <oeriksson@mandriva.com> 2.11.1-p1.2mdv2011.0
+ Revision: 619683
- the mass rebuild of 2010.0 packages

* Fri Sep 04 2009 Thierry Vignaud <tv@mandriva.org> 2.11.1-p1.1mdv2010.0
+ Revision: 429551
- rebuild

* Wed Jan 02 2008 Olivier Blin <oblin@mandriva.com> 2.11.1-p1.1mdv2008.1
+ Revision: 140792
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request


* Sun Jan 21 2007 Olivier Blin <oblin@mandriva.com> 2.11.1-p1.1mdv2007.0
+ Revision: 111318
- package ISO-3166-1 country code doc
- add update notes
- use rpm-helper service macros
- 2.11.1-p1 (and drop custom config.h)
- remove useless check in initscript
- use LSB header in init script
- Import ircd

* Thu May 12 2005 Lenny Cartier <lenny@mandrakesoft.com> 2.10.3-12mdk
- rebuild

* Fri Mar 26 2004 Lenny Cartier <lenny@mandrakesoft.com> 2.10.3-11mdk
- rebuild

* Mon Feb 23 2004 Lenny Cartier <lenny@mandrakesoft.com> 2.10.3-10mdk
- rebuild

