# Conditional build:
%bcond_with	license_agreement	# generates package
%define		source_url      http://www.mplayerhq.hu/MPlayer/releases/codecs/
#
%define		base_name	w32codec
Summary:	Binary compression/decompression libraries used by movie players
Summary(pl.UTF-8):	Binarne biblioteki do kompresji/dekompresji dla odtwarzaczy filmów
%if %{with license_agreement}
Name:		%{base_name}
%else
Name:		%{base_name}-installer
%endif
%define		_rel	2
Version:	20061022
Release:	%{_rel}%{?with_license_agreement:wla}
License:	Free for non-commercial use
Group:		Libraries
%if %{with license_agreement}
Source0:	%{source_url}all-%{version}.tar.bz2
BuildRequires:	unzip
Provides:	avi-codecs
Obsoletes:	avi-codecs
Obsoletes:	w32codec-qt
%else
Source0:	license-installer.sh
Requires:	rpm-build-tools
Requires:	unzip
Provides:	%{base_name}
%endif
AutoReqProv:	no
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
' %{SOURCE0} > $RPM_BUILD_ROOT%{_bindir}/%{base_name}.install

install %{_specdir}/%{base_name}.spec $RPM_BUILD_ROOT%{_datadir}/%{base_name}

%else
install -d $RPM_BUILD_ROOT%{_libdir}/codecs
install *.* $RPM_BUILD_ROOT%{_libdir}/codecs
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
