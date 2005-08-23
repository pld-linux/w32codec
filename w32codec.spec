#
# Conditional build:
%bcond_with	license_agreement	# generates package
#
%define		source_url	ftp://ftp1.mplayerhq.hu/MPlayer/releases/codecs/
# don't remove this macro
%define		get_version	%(cd %{tmpdir};rm -f index.html;wget --passive-ftp %{source_url}>/dev/null 2>&1;grep '>all-.*\.tar\.bz2</a>' index.html|sed -e 's:\.tar\.bz2</a>.*::' -e 's:.*>all-::'|sort|tail -n1;rm -f index.html)
Summary:	Binary compression/decompression libraries used by movie players
Summary(pl):	Binarne biblioteki do kompresji/dekompresji dla odtwarzaczy filmów
%define		base_name	w32codec
%define		_version	20050412
%if %{with license_agreement}
Name:		%{base_name}
# don't change the following line
Version:	%{_version}
%else
Name:		%{base_name}-installer
Version:	%{_version}
%endif
Release:	1%{?with_license_agreement:wla}
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
Provides:	avi-codecs
Obsoletes:	avi-codecs
Obsoletes:	w32codec-qt
BuildRequires:	unzip
%else
Requires:	cpio
Requires:	unzip
Requires:	rpm-build-tools
Requires:	wget
Provides:	%{base_name}
%endif
AutoReqProv:	no
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		w32codecDIR	ftp://ftp.pld-linux.org/dists/ac/PLD/SRPMS/SRPMS

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
Biblioteki niezbêdne do kompresji/dekompresji filmów. S± one
wykorzystywane przez odtwarzacze, ale mog± byæ u¿yte do tworzenia
kompresowanych plików z filmami.
%if %{without license_agreement}
Kwestie licencji zmusi³y nas do niedo³±czania do tego pakietu istotnych
plików. Je¶li chcesz stworzyæ w pe³ni funkcjonalny pakiet, zbuduj go za
pomoc± polecenia:

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

cat <<EOF >$RPM_BUILD_ROOT%{_bindir}/%{base_name}.install
#!/bin/sh
if [ "\$1" = "--with" -a "\$2" = "license_agreement" ]
then
	TMPDIR=\`rpm --eval "%%{tmpdir}"\`; export TMPDIR
	SPECDIR=\`rpm --eval "%%{_specdir}"\`; export SPECDIR
	SRPMDIR=\`rpm --eval "%%{_srcrpmdir}"\`; export SRPMDIR
	SOURCEDIR=\`rpm --eval "%%{_sourcedir}"\`; export SOURCEDIR
	BUILDDIR=\`rpm --eval "%%{_builddir}"\`; export BUILDDIR
	RPMDIR=\`rpm --eval "%%{_rpmdir}"\`; export RPMDIR
	BACKUP_SPEC=0
	mkdir -p \$TMPDIR \$SPECDIR \$SRPMDIR \$RPMDIR \$SRPMDIR \$SOURCEDIR \$BUILDDIR
	if [ -f \$SPECDIR/%{base_name}.spec ]; then
		BACKUP_SPEC=1
		mv -f \$SPECDIR/%{base_name}.spec \$SPECDIR/%{base_name}.spec.prev
	fi
	if echo "\$3" | grep '\.src\.rpm$' >/dev/null; then
		( cd \$SRPMDIR
		if echo "\$3" | grep '://' >/dev/null; then
			wget --passive-ftp -t0 "\$3"
		else
			cp -f "\$3" .
		fi
		rpm2cpio \`basename "\$3"\` | ( cd \$TMPDIR; cpio -i %{base_name}.spec ) )
		if ! cp -i \$TMPDIR/%{base_name}.spec \$SPECDIR/%{base_name}.spec; then
			exit 1
		fi
	else
		if ! cp -i "\$3" \$SPECDIR; then
			exit 1
		fi
	fi
	( cd \$SPECDIR
	%{_bindir}/builder -nc -ncs --with license_agreement --opts --target=%{_target_cpu} %{base_name}.spec
	if [ "\$?" -ne 0 ]; then
		exit 2
	fi
	RPMNAME=\$(cd \$RPMDIR;ls -t %{base_name}-*-%{release}wla.%{_target_cpu}.rpm|head -n1)
	rpm -U \$RPMDIR/\$RPMNAME || \
		echo -e Install manually the file:\\\n   \$RPMDIR/\$RPMNAME )
	if [ "\$BACKUP_SPEC" -eq 1 ]; then
		mv -f \$SPECDIR/%{base_name}.spec.prev \$SPECDIR/%{base_name}.spec
	fi
else
	echo "
License issues made us not to include inherent files into
this package by default. If you want to create full working
package please build it with the following command:

\$0 --with license_agreement %{_datadir}/%{base_name}/%{base_name}.spec
"
fi
EOF

sed '0,/^Version:.*%%{_version}/s/{_version}/{get_version}/' < %{_specdir}/%{base_name}.spec > $RPM_BUILD_ROOT%{_datadir}/%{base_name}/%{base_name}.spec

%else
install -d $RPM_BUILD_ROOT%{_libdir}/codecs
install *.* $RPM_BUILD_ROOT%{_libdir}/codecs
rm -f $RPM_BUILD_ROOT%{_libdir}/codecs/*_linuxELFx86c6.xa
%endif

%if %{without license_agreement}
%pre
echo "
License issues made us not to include inherent files into
this package by default. If you want to create full working
package please build it with the following command:

%{base_name}.install --with license_agreement %{_datadir}/%{base_name}/%{base_name}.spec
"
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
