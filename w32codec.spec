#
# Conditional build:
# _with_license_agreement	- creates nonempty package
#				- (read below for details)
#
Summary:	Windows compression/decompression libraries used by movie players
Summary(pl):	Windziane biblioteki do kompresji/dekompresji dla odtwarzaczy filmów
Name:		w32codec
Version:	0.18
Release:	2
Group:		Libraries
Group(de):	Libraries
Group(es):	Bibliotecas
Group(fr):	Librairies
Group(pl):	Biblioteki
License:	Mostly freeware, some free for non-commercial use.
%{?_with_license_agreement:Source0:	http://mplayerhq.banki.hu/MPlayer/releases/%{name}-%{version}.zip}
BuildRequires:	unzip
Autoreqprov:	false
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	avi-codecs

%description
Libraries required to compress/decompress content of movie files. They
are used by movie players, but can be used to create compressed movie
files.

%{?!_with_license_agreement:License issues made us not to include inherent files into}
%{?!_with_license_agreement:this package by default. If you want to create full working}
%{?!_with_license_agreement:package please build it with the following command:}
%{?!_with_license_agreement:}
%{?!_with_license_agreement:rpm --rebuild --with license_agreement ftp://ftp.pld.org.pl/PLD-1.0/SRPMS/SRPMS/%{name}-%{version}-%{release}.nosrc.rpm}

%description -l pl
Biblioteki niezbêdne do kompresji/dekompresji filmów.
S± one wykorzystywane przez odtwarzacze, ale mog± byæ u¿yte do
tworzenia skompresowanych plików z filmami.

%{?!_with_license_agreement:Kwestie licencji zmusi³y nas do niedo³±czania do tego}
%{?!_with_license_agreement:pakietu istotnych plików. Je¶li chcesz stworzyæ w pe³ni}
%{?!_with_license_agreement:funkcjonalny pakiet zbuduj go za pomoc± komendy:}
%{?!_with_license_agreement:}
%{?!_with_license_agreement:rpm --rebuild --with license_agreement ftp://ftp.pld.org.pl/PLD-1.0/SRPMS/SRPMS/%{name}-%{version}-%{release}.nosrc.rpm}

%prep

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_libdir}/win32

%{?_with_license_agreement:echo "A" | unzip -q %{SOURCE0} -d $RPM_BUILD_ROOT%{_libdir}/win32}

%pre
%{?!_with_license_agreement:echo "}
%{?!_with_license_agreement:License issues made us not to include inherent files into}
%{?!_with_license_agreement:this package by default. If you want to create full working}
%{?!_with_license_agreement:package please build it with the following command:}
%{?!_with_license_agreement:}
%{?!_with_license_agreement:rpm --rebuild --with license_agreement ftp://ftp.pld.org.pl/PLD-1.0/SRPMS/SRPMS/%{name}-%{version}-%{release}.nosrc.rpm}
%{?!_with_license_agreement:"}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%dir %{_libdir}/win32
%{?_with_license_agreement:%{_libdir}/win32/*}
