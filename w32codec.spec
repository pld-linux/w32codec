#
# Conditional build:
# _with_license_agreement	- generates package

Summary:	Windows compression/decompression libraries used by movie players
Summary(pl):	Windziane biblioteki do kompresji/dekompresji dla odtwarzaczy filmÛw
Name:		w32codec
Version:	0.50
Release:	2
Group:		Libraries
Group(de):	Libraries
Group(es):	Bibliotecas
Group(fr):	Librairies
Group(pl):	Biblioteki
Group(pt_BR):	Bibliotecas
Group(ru):	‚…¬Ã…œ‘≈À…
Group(uk):	‚¶¬Ã¶œ‘≈À…
License:	Mostly freeware, some free for non-commercial use.
%{?_with_license_agreement:Source0:	http://mplayerhq.banki.hu/MPlayer/releases/%{name}-%{version}.zip}
BuildRequires:	unzip
Autoreqprov:	false
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Provides:	avi-codecs
Obsoletes:	avi-codecs

%description
Libraries required to compress/decompress content of movie files. They
are used by movie players, but can be used to create compressed movie
files.

%description -l pl
Biblioteki niezbÍdne do kompresji/dekompresji filmÛw. S± one
wykorzystywane przez odtwarzacze, ale mog± byÊ uøyte do
tworzenia kompresowanych plikÛw z filmami.

%prep
%{!?_with_license_agreement:exit 1}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/win32

echo "A" | unzip -q %{SOURCE0} -d $RPM_BUILD_ROOT%{_libdir}/win32

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{_libdir}/win32
