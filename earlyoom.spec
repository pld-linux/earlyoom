Summary:	Early OOM Daemon for Linux
Name:		earlyoom
Version:	1.7
Release:	0.1
License:	MIT
URL:		https://github.com/rfjakob/earlyoom
Source0:	https://github.com/rfjakob/earlyoom/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	9c567930c60b2ccdc536951b005d413d
Source1:	%{name}.conf

%description
User-space OOM killer daemon that can avoid the system going into the
unresponsive state. It checks the amount of available memory and free
swap up to 10 times a second (less often if there is a lot of free
memory) and kills the largest processes with the highest oom_score.

Percentages are configured through the configuration file.

%prep
%setup -q
cp -f %{SOURCE1} %{name}.default
sed -e '/systemctl/d' -i Makefile

%build
%{__make} \
	VERSION=%{version} \
	PREFIX=%{_prefix} \
	SYSCONFDIR=%{_sysconfdir} \
	SYSTEMDUNITDIR=%{systemdunitdir}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/%{name}
%{systemdunitdir}/%{name}.service
%{_mandir}/man1/%{name}.*
%config(noreplace) %{_sysconfdir}/default/%{name}

