# Conditional build:
%bcond_with	license_agreement	# generates package
#
#%define		source_url	ftp://ftp1.mplayerhq.hu/MPlayer/releases/codecs/
%define		source_url	ftp://ftp2.mplayerhq.hu/MPlayer/releases/codecs/
Summary:	Binary compression/decompression libraries used by movie players
Summary(pl):	Binarne biblioteki do kompresji/dekompresji dla odtwarzaczy film�w
%define		base_name	w32codec
%if %{with license_agreement}
Name:		%{base_name}
%else
Name:		%{base_name}-installer
%endif
Version:	20050412
Release:	1.3%{?with_license_agreement:wla}
Group:		Libraries
License:	Free for non-commercial use
%if %{with license_agreement}
Source0:	%{source_url}all-%{version}.tar.bz2
#Source1:	%{source_url}qt6dlls.tar.bz2
#Source2:	%{source_url}qtextras.tar.bz2
#Source3:	%{source_url}rp8codecs.tar.bz2
#Source4:	%{source_url}rp9codecs.tar.bz2
#Source5:	%{source_url}xanimdlls.tar.bz2
Source6:	http://www.ezgoal.com/dll_files/tsd32.zip
BuildRequires:	unzip
Provides:	avi-codecs
Obsoletes:	avi-codecs
Obsoletes:	w32codec-qt
NoSource:	0
NoSource:	6
%else
Source0:	license-installer.sh
Requires:	cpio
Requires:	rpm-build-tools
Requires:	unzip
Requires:	wget
Provides:	%{base_name}
%endif
AutoReqProv:	no
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Libraries required to compress/decompress content of movie files. They
are used by movie players, but can be used to create compressed movie
files.
%if %{without license_agreement}
License issues made us not to include inherent files into this package
by default. If you want to create full working package please build it
with the following command:

%{base_name}.install --with license_agreement %{_datadir}/%{base_name}/%{base_name}.spec
%endif

%description -l pl
Biblioteki niezb�dne do kompresji/dekompresji film�w. S� one
wykorzystywane przez odtwarzacze, ale mog� by� u�yte do tworzenia
kompresowanych plik�w z filmami.
%if %{without license_agreement}
Kwestie licencji zmusi�y nas do niedo��czania do tego pakietu istotnych
plik�w. Je�li chcesz stworzy� w pe�ni funkcjonalny pakiet, zbuduj go za
pomoc� polecenia:

%{base_name}.install --with license_agreement %{_datadir}/%{base_name}/%{base_name}.spec
%endif

%prep
%if %{with license_agreement}
%setup -q -n all-%{version}
#bzcat %{SOURCE1} | tar xf -
#bzcat %{SOURCE2} | tar xf -
#bzcat %{SOURCE3} | tar xf -
#bzcat %{SOURCE4} | tar xf -
#bzcat %{SOURCE5} | tar xf -
unzip %{SOURCE6}
mv TSD32.DLL tsd32.dll
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
%pre
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
