#
# Conditional build:
# _with_license_agreement	- generates package

Summary:	Windows compression/decompression libraries used by movie players
Summary(pl):	Windziane biblioteki do kompresji/dekompresji dla odtwarzaczy filmów
Name:		w32codec
Version:	0.60
Release:	5
Group:		Libraries
License:	Free for non-commercial use
%{?_with_license_agreement:Source0:	http://www.mplayerhq.hu/MPlayer/releases/%{name}-%{version}.tar.bz2}
Autoreqprov:	false
ExclusiveArch:	%{ix86}
Provides:	avi-codecs
Obsoletes:	avi-codecs
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Libraries required to compress/decompress content of movie files. They
are used by movie players, but can be used to create compressed movie
files.

%{?!_with_license_agreement:License issues made us not to include inherent files into}
%{?!_with_license_agreement:this package by default. If you want to create full working}
%{?!_with_license_agreement:package please build it with the following command:}
%{?!_with_license_agreement:}
%{?!_with_license_agreement:rpm --rebuild --with license_agreement ftp://ftp.pld.org.pl/dists/ra/PLD/SRPMS/SRPMS/%{name}-%{version}-%{release}.src.rpm}

%description -l pl
Biblioteki niezbêdne do kompresji/dekompresji filmów. S± one
wykorzystywane przez odtwarzacze, ale mog± byæ u¿yte do tworzenia
kompresowanych plików z filmami.

%{?!_with_license_agreement:Kwestie licencji zmusi³y nas do niedo³±czania do tego}
%{?!_with_license_agreement:pakietu istotnych plików. Je¶li chcesz stworzyæ w pe³ni}
%{?!_with_license_agreement:funkcjonalny pakiet zbuduj go za pomoc± komendy:}
%{?!_with_license_agreement:}
%{?!_with_license_agreement:rpm --rebuild --with license_agreement ftp://ftp.pld.org.pl/dists/ra/PLD/SRPMS/SRPMS/%{name}-%{version}-%{release}.src.rpm}

%prep
%{?_with_license_agreement:%setup -q}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/win32

%{?_with_license_agreement:install * $RPM_BUILD_ROOT%{_libdir}/win32}

%pre
%{?!_with_license_agreement:echo "}
%{?!_with_license_agreement:License issues made us not to include inherent files into}
%{?!_with_license_agreement:this package by default. If you want to create full working}
%{?!_with_license_agreement:package please build it with the following command:}
%{?!_with_license_agreement:}
%{?!_with_license_agreement:rpm --rebuild --with license_agreement ftp://ftp.pld.org.pl/dists/ra/PLD/SRPMS/SRPMS/%{name}-%{version}-%{release}.src.rpm}
%{?!_with_license_agreement:"}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{_libdir}/win32
