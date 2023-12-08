Summary:	Early OOM Daemon for Linux
Name:		earlyoom
Version:	1.7
Release:	1
License:	MIT
URL:		https://github.com/rfjakob/earlyoom
Source0:	https://github.com/rfjakob/earlyoom/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	9c567930c60b2ccdc536951b005d413d
Source1:	%{name}.conf
Source2:	%{name}.init
BuildRequires:	pandoc
Requires(post,preun):	/sbin/chkconfig
Requires:	systemd-units
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
User-space OOM killer daemon that can avoid the system going into the
unresponsive state. It checks the amount of available memory and free
swap up to 10 times a second (less often if there is a lot of free
memory) and kills the largest processes with the highest oom_score.

Percentages are configured through the configuration file.

%prep
%setup -q
cp -f %{SOURCE1} %{name}.default
sed -i -e '/systemctl/d' Makefile
sed -i -e 's#/default/#/sysconfig/#g' Makefile earlyoom.service.in

%build
%{__make} \
	VERSION=%{version} \
	BINDIR=/bin \
	PREFIX=%{_prefix} \
	SYSCONFDIR=%{_sysconfdir} \
	SYSTEMDUNITDIR=%{systemdunitdir}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/rc.d/init.d

%{__make} install \
	PREFIX=%{_prefix} \
	BINDIR=/bin \
	SYSCONFDIR=%{_sysconfdir} \
	SYSTEMDUNITDIR=%{systemdunitdir} \
	DESTDIR=$RPM_BUILD_ROOT

cp -a %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
%service %{name} restart
%systemd_post %{name}.service

%preun
if [ "$1" = "0" ]; then
        %service %{name} stop
        /sbin/chkconfig --del %{name}
fi
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%defattr(644,root,root,755)
%doc README.md
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(755,root,root) %{_bindir}/%{name}
%{systemdunitdir}/%{name}.service
%{_mandir}/man1/%{name}.*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}

