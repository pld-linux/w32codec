#
# Conditional build:
# _with_license_agreement	- generates package

Summary:	Windows compression/decompression libraries used by movie players
Summary(pl):	Windziane biblioteki do kompresji/dekompresji dla odtwarzaczy filmów
Name:		w32codec
Version:	0.60
Release:	2
Group:		Libraries
License:	Mostly freeware, some free for non-commercial use.
%{?_with_license_agreement:Source0:	http://mplayerhq.banki.hu/MPlayer/releases/%{name}-%{version}.tar.bz2}
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
Biblioteki niezbêdne do kompresji/dekompresji filmów. S± one
wykorzystywane przez odtwarzacze, ale mog± byæ u¿yte do
tworzenia kompresowanych plików z filmami.

%prep
%{!?_with_license_agreement:exit 1}
%setup -q

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_libdir}/win32
install * $RPM_BUILD_ROOT%{_libdir}/win32

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{_libdir}/win32
