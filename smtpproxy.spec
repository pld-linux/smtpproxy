Summary:	An application level gateway for the SMTP protocol
Summary(pl):	Brama warstwy aplikacji dla protoko�u SMTP
Name:		smtpproxy
Version:	1.1.3
Release:	3
License:	GPL
Group:		Applications/Networking
Source0:	http://www.quietsche-entchen.de/download/%{name}-%{version}.tar.gz
# Source0-md5:	c4558c8d379644e5b1fd66c389107a1e
Source1:	%{name}.inetd
Prereq:		rc-inetd >= 0.8.1
URL:		http://www.quietsche-entchen.de/software/smtp.proxy.html
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Conflicts:	proxytools

%description
smtp.proxy is an application level gateway for the SMTP protocol based
on the specification in RFC 821. It also supports some commands that
came with later RFCs. Unlike generic TCP proxys smtp.proxy looks into
the data streams it forward and watches over the protocol.

%description -l pl
smtp.proxy jest aplikacyjn� bramk� dla protoko�u SMTP. W odr�nieniu
od innych tego typu program�w, smtpproxy nadzoruje transmisj�
sprawdzaj�c czy klient i serwer spe�niaj� specyfikacj� protoko�u (RFC
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
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload 1>&2
else
	echo "Type \"/etc/rc.d/init.d/rc-inetd start\" to start inet server" 1>&2
fi

%postun
if [ "$1" = "0" -a -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload
fi

%files
%defattr(644,root,root,755)
%doc README rfc821.txt
%attr(640,root,root) %config %verify(not size mtime md5) /etc/sysconfig/rc-inetd/smtpproxy
%attr(755,root,root) %{_sbindir}/smtp.proxy
%{_mandir}/man1/*