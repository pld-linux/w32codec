# TODO
# - http://security.gentoo.org/glsa/glsa-200803-08.xml
#
# Conditional build:
%bcond_with	license_agreement	# generates package
%define		source_url	http://www.mplayerhq.hu/MPlayer/releases/codecs

%define		base_name	w32codec
%define		rel	1
Summary:	Binary compression/decompression libraries used by movie players
Summary(pl.UTF-8):	Binarne biblioteki do kompresji/dekompresji dla odtwarzaczy filmów
%if %{with license_agreement}
Name:		%{base_name}
%else
Name:		%{base_name}-installer
%endif
Version:	20110131
Release:	%{rel}%{?with_license_agreement:wla}
License:	Free for non-commercial use
Group:		Libraries
%if %{with license_agreement}
Source0:	%{source_url}/all-%{version}.tar.bz2
# NoSource0-md5:	303cf3cbf15e7084d1cfed3f0e3ef8e4
NoSource:	0
Provides:	avi-codecs
Obsoletes:	avi-codecs
Obsoletes:	w32codec-qt
%else
Source1:	http://svn.pld-linux.org/svn/license-installer/license-installer.sh
# Source1-md5:	329c25f457fea66ec502b7ef70cb9ede
Requires:	rpm-build-tools >= 4.4.37
Requires:	rpmbuild(macros) >= 1.544
Provides:	%{base_name}
%endif
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
AutoReqProv:	no

# avoid empty debuginfo package
%define		_enable_debug_packages	0

%description
Libraries required to compress/decompress content of movie files. They
are used by movie players, but can be used to create compressed movie
files.

%description -l pl.UTF-8
Biblioteki niezbędne do kompresji/dekompresji filmów. Są one
wykorzystywane przez odtwarzacze, ale mogą być użyte do tworzenia
kompresowanych plików z filmami.

%prep
%if %{with license_agreement}
%setup -q -n all-%{version}
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{without license_agreement}
install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/%{base_name}}

sed -e '
	s/@BASE_NAME@/%{base_name}/g
	s/@TARGET_CPU@/%{_target_cpu}/g
	s-@VERSION@-%{version}-g
	s-@RELEASE@-%{release}-g
	s,@SPECFILE@,%{_datadir}/%{base_name}/%{base_name}.spec,g
	s,@DATADIR@,%{_datadir}/%{base_name},g
' %{SOURCE1} > $RPM_BUILD_ROOT%{_bindir}/%{base_name}.install
chmod +x $RPM_BUILD_ROOT%{_bindir}/%{base_name}.install

cp -a %{_specdir}/%{base_name}.spec $RPM_BUILD_ROOT%{_datadir}/%{base_name}

%else
install -d $RPM_BUILD_ROOT%{_libdir}/codecs
cp -a *.* $RPM_BUILD_ROOT%{_libdir}/codecs
# essential of these are in in linuxcodec.spec
# (i.e. all except {atrc,cook,ddnt,dnet,drv[234]}.so.6.0 from rp9codecs-20050115 and vid_{cvid,cyuv,h26[13],iv{32,41,50}}.xa from xanimdlls-20040626
rm -f $RPM_BUILD_ROOT%{_libdir}/codecs/*.so*
rm -f $RPM_BUILD_ROOT%{_libdir}/codecs/*.xa
%endif

%if %{without license_agreement}
%post
%{_bindir}/%{base_name}.install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%if %{with license_agreement}
%{_libdir}/codecs
%else
%attr(755,root,root) %{_bindir}/w32codec.install
%{_datadir}/%{base_name}
%endif
