#
# Conditional build:
# _with_license_agreement	- generates package
#
Summary:	Windows compression/decompression libraries used by movie players
Summary(pl):	Windziane biblioteki do kompresji/dekompresji dla odtwarzaczy filmów
Name:		w32codec
Version:	0.90pre7
Release:	4%{?_with_license_agreement:wla}
Group:		Libraries
License:	Free for non-commercial use
%{?_with_license_agreement:Source0:	http://www.mplayerhq.hu/MPlayer/releases/%{name}-%{version}.tar.bz2}
%{?_with_license_agreement:Source1:	http://www1.mplayerhq.hu/MPlayer/releases/codecs/qt6dlls.tar.bz2}
%{?_with_license_agreement:Source2:	http://www1.mplayerhq.hu/MPlayer/releases/codecs/qtextras.tar.bz2}
%{?_with_license_agreement:Source3:	http://www1.mplayerhq.hu/MPlayer/releases/codecs/rp8codecs.tar.bz2}
%{?_with_license_agreement:Source4:	http://www1.mplayerhq.hu/MPlayer/releases/codecs/rp9codecs.tar.bz2}
%{?_with_license_agreement:Source5:	http://www1.mplayerhq.hu/MPlayer/releases/codecs/xanimdlls.tar.bz2}
Autoreqprov:	false
ExclusiveArch:	%{ix86}
%{?!_with_license_agreement:Requires:	wget}
%{?!_with_license_agreement:Requires:	rpm-build-tools}
%{?_with_license_agreement:Provides:	avi-codecs}
%{?_with_license_agreement:Obsoletes:	avi-codecs}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

#%%define		w32codecDIR	ftp://ftp.pld.org.pl/dists/ra/test/SRPMS/
%define		w32codecDIR	ftp://ftp.pld.org.pl/dists/ra/PLD/SRPMS/SRPMS/

%description
Libraries required to compress/decompress content of movie files. They
are used by movie players, but can be used to create compressed movie
files.
%if %{?!_with_license_agreement:1}%{?_with_license_agreement:0}
License issues made us not to include inherent files into this package
by default. If you want to create full working package please build it
with the following command:

w32codec.install --with license_agreement %{w32codecDIR}/%{name}-%{version}-%{release}.src.rpm
%endif

%description -l pl
Biblioteki niezbêdne do kompresji/dekompresji filmów. S± one
wykorzystywane przez odtwarzacze, ale mog± byæ u¿yte do tworzenia
kompresowanych plików z filmami.
%if %{?!_with_license_agreement:1}%{?_with_license_agreement:0}
Kwestie licencji zmusi³y nas do niedo³±czania do tego pakietu istotnych
plików. Je¶li chcesz stworzyæ w pe³ni funkcjonalny pakiet, zbuduj go za
pomoc± polecenia:

w32codec.install --with license_agreement %{w32codecDIR}/%{name}-%{version}-%{release}.src.rpm
%endif

%prep
%{?_with_license_agreement:%setup -q -n %{name}-0.90}

install_codecs() {
	bzcat %{SOURCE1} | tar xf -
	bzcat %{SOURCE2} | tar xf -
	bzcat %{SOURCE3} | tar xf -
	bzcat %{SOURCE4} | tar xf -
	bzcat %{SOURCE5} | tar xf -

	for f in */*; do mv $f .; done
}

%{?_with_license_agreement:install_codecs}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/win32

%if %{?_with_license_agreement:0}%{?!_with_license_agreement:1}
install -d $RPM_BUILD_ROOT%{_bindir}
cat <<EOF >$RPM_BUILD_ROOT%{_bindir}/w32codec.install
#!/bin/sh
if [ "\$1" = "--with" -a "\$2" = "license_agreement" ]
then
	TMPDIR=\`rpm --eval "%%{tmpdir}"\`; export TMPDIR
	SPECDIR=\`rpm --eval "%%{_specdir}"\`; export SPECDIR
	SRPMDIR=\`rpm --eval "%%{_srcrpmdir}"\`; export SRPMDIR
	RPMDIR=\`rpm --eval "%%{_rpmdir}"\`; export RPMDIR
	( cd \$SRPMDIR
	if echo "\$3" | grep '://' >/dev/null
	then
		wget -t0 "\$3"
	else
		cp -f "\$3" .
	fi
	rpm2cpio \`basename "\$3"\` | ( cd \$TMPDIR; cpio -i w32codec.spec ) )
	if ! cp -i \$TMPDIR/w32codec.spec \$SPECDIR/w32codec.spec; then
		exit 1
	fi
	( cd \$SPECDIR
	%{_bindir}/builder -nc -ncs --with license_agreement --opts --target=%{_target_cpu} w32codec.spec
	rpm -U \$RPMDIR/%{name}-%{version}-%{release}wla.%{_target_cpu}.rpm || \
		echo -e Install manually the file:\\\n   \$RPMDIR/%{name}-%{version}-%{release}wla.%{_target_cpu}.rpm )
else
	echo "
License issues made us not to include inherent files into
this package by default. If you want to create full working
package please build it with the following command:

\$0 --with license_agreement %{w32codecDIR}/%{name}-%{version}-%{release}.src.rpm
"
fi
EOF
%else
install *.* $RPM_BUILD_ROOT%{_libdir}/win32
%endif

%pre
%if %{?!_with_license_agreement:1}%{?_with_license_agreement:0}
echo "
License issues made us not to include inherent files into
this package by default. If you want to create full working
package please build it with the following command:

w32codec.install --with license_agreement %{w32codecDIR}/%{name}-%{version}-%{release}.src.rpm
"
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{?_with_license_agreement:%{_libdir}/win32}
%{?!_with_license_agreement:%attr(755,root,root) %{_bindir}/w32codec.install}
