Summary:	An application level gateway for the SMTP protocol
Summary(pl.UTF-8):	Brama warstwy aplikacji dla protokołu SMTP
Name:		smtpproxy
Version:	1.1.3
Release:	3
License:	GPL
Group:		Networking/Daemons/SMTP
Source0:	http://www.quietsche-entchen.de/download/%{name}-%{version}.tar.gz
# Source0-md5:	c4558c8d379644e5b1fd66c389107a1e
Source1:	%{name}.inetd
URL:		http://www.quietsche-entchen.de/software/smtp.proxy.html
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	rc-inetd >= 0.8.1
Conflicts:	proxytools
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
smtp.proxy is an application level gateway for the SMTP protocol based
on the specification in RFC 821. It also supports some commands that
came with later RFCs. Unlike generic TCP proxys smtp.proxy looks into
the data streams it forward and watches over the protocol.

%description -l pl.UTF-8
smtp.proxy jest aplikacyjną bramką dla protokołu SMTP. W odróżnieniu
od innych tego typu programów, smtpproxy nadzoruje transmisję
sprawdzając czy klient i serwer spełniają specyfikację protokołu (RFC
821).

%prep
%setup -q

%build
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man1,/etc/sysconfig/rc-inetd}

install smtp.proxy $RPM_BUILD_ROOT%{_sbindir}
install smtp.proxy.1 $RPM_BUILD_ROOT%{_mandir}/man1

install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/smtpproxy

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q rc-inetd reload

%postun
if [ "$1" = "0" ]; then
	%service -q rc-inetd reload
fi

%files
%defattr(644,root,root,755)
%doc README rfc821.txt
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/rc-inetd/smtpproxy
%attr(755,root,root) %{_sbindir}/smtp.proxy
%{_mandir}/man1/*
