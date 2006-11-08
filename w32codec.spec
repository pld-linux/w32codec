# TODO:
#   ppc support
#
# Conditional build:
%bcond_with	license_agreement	# generates package
%define		source_url      http://www4.mplayerhq.hu/MPlayer/releases/codecs/
#
%define		base_name	w32codec
Summary:	Binary compression/decompression libraries used by movie players
Summary(pl):	Binarne biblioteki do kompresji/dekompresji dla odtwarzaczy filmów
%if %{with license_agreement}
Name:		%{base_name}
%else
Name:		%{base_name}-installer
%endif
%define		_rel	1
Version:	20061022
Release:	%{_rel}%{?with_license_agreement:wla}
License:	Free for non-commercial use
Group:		Libraries
%if %{with license_agreement}
Source0:	%{source_url}all-%{version}.tar.bz2
#Source1:	%{source_url}qt6dlls.tar.bz2
#Source2:	%{source_url}qtextras.tar.bz2
#Source3:	%{source_url}rp8codecs.tar.bz2
#Source4:	%{source_url}rp9codecs.tar.bz2
#Source5:	%{source_url}xanimdlls.tar.bz2
#Source6:	http://www.ezgoal.com/dll_files/tsd32.zip
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

%description -l pl
Biblioteki niezbêdne do kompresji/dekompresji filmów. S± one
wykorzystywane przez odtwarzacze, ale mog± byæ u¿yte do tworzenia
kompresowanych plików z filmami.

%prep
%if %{with license_agreement}
%setup -q -n all-%{version}
#bzcat %{SOURCE1} | tar xf -
#bzcat %{SOURCE2} | tar xf -
#bzcat %{SOURCE3} | tar xf -
#bzcat %{SOURCE4} | tar xf -
#bzcat %{SOURCE5} | tar xf -
#unzip %{SOURCE6}
#mv TSD32.DLL tsd32.dll
#for f in */*; do mv $f .; done
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
rm -f $RPM_BUILD_ROOT%{_libdir}/codecs/*_linuxELFx86c6.xa
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
