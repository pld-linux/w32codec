#
# Conditional build:
%bcond_with	license_agreement	# generates package
#
Summary:	Binary compression/decompression libraries used by movie players
Summary(pl):	Binarne biblioteki do kompresji/dekompresji dla odtwarzaczy filmów
Name:		w32codec
Version:	20041107
Release:	1%{?with_license_agreement:wla}
Group:		Libraries
License:	Free for non-commercial use
%if %{with license_agreement}
Source0:	ftp://ftp1.mplayerhq.hu/MPlayer/releases/codecs/all-%{version}.tar.bz2
#Source1:	ftp://ftp1.mplayerhq.hu/MPlayer/releases/codecs/qt6dlls.tar.bz2
#Source2:	ftp://ftp1.mplayerhq.hu/MPlayer/releases/codecs/qtextras.tar.bz2
#Source3:	ftp://ftp1.mplayerhq.hu/MPlayer/releases/codecs/rp8codecs.tar.bz2
#Source4:	ftp://ftp1.mplayerhq.hu/MPlayer/releases/codecs/rp9codecs.tar.bz2
#Source5:	ftp://ftp1.mplayerhq.hu/MPlayer/releases/codecs/xanimdlls.tar.bz2
Source6:	http://www.ezgoal.com/dll_files/tsd32.zip
Provides:	avi-codecs
Obsoletes:	avi-codecs
Obsoletes:	w32codec-qt
BuildRequires:	unzip
%else
Requires:	cpio
Requires:	unzip
Requires:	rpm-build-tools
Requires:	wget
%endif
AutoReqProv:	no
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		w32codecDIR	ftp://ftp.pld-linux.org/dists/ac/PLD/SRPMS/SRPMS

%description
Libraries required to compress/decompress content of movie files. They
are used by movie players, but can be used to create compressed movie
files.
%if ! %{with license_agreement}
License issues made us not to include inherent files into this package
by default. If you want to create full working package please build it
with the following command:

w32codec.install --with license_agreement %{w32codecDIR}/%{name}-%{version}-%{release}.src.rpm
%endif

%description -l pl
Biblioteki niezbêdne do kompresji/dekompresji filmów. S± one
wykorzystywane przez odtwarzacze, ale mog± byæ u¿yte do tworzenia
kompresowanych plików z filmami.
%if ! %{with license_agreement}
Kwestie licencji zmusi³y nas do niedo³±czania do tego pakietu istotnych
plików. Je¶li chcesz stworzyæ w pe³ni funkcjonalny pakiet, zbuduj go za
pomoc± polecenia:

w32codec.install --with license_agreement %{w32codecDIR}/%{name}-%{version}-%{release}.src.rpm
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

%if ! %{with license_agreement}
install -d $RPM_BUILD_ROOT%{_bindir}
cat <<EOF >$RPM_BUILD_ROOT%{_bindir}/w32codec.install
#!/bin/sh
if [ "\$1" = "--with" -a "\$2" = "license_agreement" ]
then
	TMPDIR=\`rpm --eval "%%{tmpdir}"\`; export TMPDIR
	SPECDIR=\`rpm --eval "%%{_specdir}"\`; export SPECDIR
	SRPMDIR=\`rpm --eval "%%{_srcrpmdir}"\`; export SRPMDIR
	SOURCEDIR=\`rpm --eval "%%{_sourcedir}"\`; export SOURCEDIR
	BUILDDIR=\`rpm --eval "%%{_builddir}"\`; export BUILDDIR
	RPMDIR=\`rpm --eval "%%{_rpmdir}"\`; export RPMDIR
	mkdir -p \$TMPDIR \$SPECDIR \$SRPMDIR \$RPMDIR \$SRPMDIR \$SOURCEDIR \$BUILDDIR
	( cd \$SRPMDIR
	if echo "\$3" | grep '://' >/dev/null
	then
		wget --passive-ftp -t0 "\$3"
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
install -d $RPM_BUILD_ROOT%{_libdir}/codecs
install *.* $RPM_BUILD_ROOT%{_libdir}/codecs
rm -f $RPM_BUILD_ROOT%{_libdir}/codecs/*_linuxELFx86c6.xa
%endif

%if ! %{with license_agreement}
%pre
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
%{?with_license_agreement:%{_libdir}/codecs}
%{!?with_license_agreement:%attr(755,root,root) %{_bindir}/w32codec.install}
