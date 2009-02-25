# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define _with_gcj_support 1
%define gcj_support %{?_with_gcj_support:1}%{!?_with_gcj_support:%{?_without_gcj_support:0}%{!?_without_gcj_support:%{?_gcj_support:%{_gcj_support}}%{!?_gcj_support:0}}}

# If you don't want to build with maven, and use straight ant instead,
# give rpmbuild option '--without maven'

%define _without_maven 1

%define with_maven %{!?_without_maven:1}%{?_without_maven:0}
%define without_maven %{?_without_maven:1}%{!?_without_maven:0}

%define maven_settings_file %{_builddir}/%{name}/settings.xml

Name:           maven-surefire
Version:        1.5.3
Release:        3.8%{?dist}
Epoch:          0
Summary:        Test framework project
License:        ASL 2.0
Group:          Development/Java
URL:            http://maven.apache.org/surefire/

# svn export
#    http://svn.apache.org/repos/asf/maven/surefire/tags/surefire-1.5.3/ 
#    surefire/
# tar czf surefire-tar.gz surefire/
# svn export 
#    http://svn.apache.org/repos/asf/maven/surefire/tags/surefire-booter-1.5.3/
#    surefire-booter/
# tar czf surefire-booter-tar.gz surefire-booter/
Source0:        %{name}-%{version}.tar.gz
Source1:        %{name}-booter-%{version}.tar.gz

Source2:        %{name}-build.xml
Source3:        %{name}-booter-build.xml
Source4:        %{name}-jpp-depmap.xml

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%if ! %{gcj_support}
BuildArch:      noarch
%endif

BuildRequires:  ant
BuildRequires:  ant-nodeps
BuildRequires:  classworlds
BuildRequires:  jpackage-utils >= 0:1.7.2
BuildRequires:  junit >= 3.8.2
BuildRequires:  plexus-utils

%if %{with_maven}
BuildRequires:  maven2 >= 2.0.4-9
BuildRequires:  maven2-plugin-compiler
BuildRequires:  maven2-plugin-install
BuildRequires:  maven2-plugin-jar
BuildRequires:  maven2-plugin-javadoc
BuildRequires:  maven2-plugin-resources
BuildRequires:  maven2-plugin-surefire
%endif

Requires:       classworlds
Requires:       plexus-utils
Requires:       junit

Requires(post):    jpackage-utils >= 0:1.7.2
Requires(postun):  jpackage-utils >= 0:1.7.2

%if %{gcj_support}
BuildRequires:          java-gcj-compat-devel
Requires(post):         java-gcj-compat
Requires(postun):       java-gcj-compat
%endif

%description
Surefire is a test framework project.

%package booter
Summary:                Booter for %{name}
Group:                  Development/Java
Requires:               maven-surefire = %{epoch}:%{version}-%{release}

%if %{gcj_support}
BuildRequires:          java-gcj-compat-devel
Requires(post):         java-gcj-compat
Requires(postun):       java-gcj-compat
%endif

%description booter
Surefire is a test framework project.

%if %{with_maven}
%package javadoc
Summary:          Javadoc for %{name}
Group:            Development/Documentation
# for /bin/rm and /bin/ln
Requires(post):   coreutils
Requires(postun): coreutils

%description javadoc
Javadoc for %{name}.

%package booter-javadoc
Summary:          Javadoc for %{name}
Group:            Development/Documentation
# for /bin/rm and /bin/ln
Requires(post):   coreutils
Requires(postun): coreutils

%description booter-javadoc
Javadoc for %{name}.
%endif

%prep
%setup -q -c -n %{name}

tar xzf %{SOURCE1}

cp -p %{SOURCE2} surefire/build.xml
cp -p %{SOURCE3} surefire-booter/build.xml

sed -i -e s:"static private void failSame(":"static public void failSame(":g surefire/src/main/java/org/apache/maven/surefire/battery/assertion/BatteryAssert.java
sed -i -e s:"static private void failNotSame(":"static public void failNotSame(":g surefire/src/main/java/org/apache/maven/surefire/battery/assertion/BatteryAssert.java
sed -i -e s:"static private void failNotEquals(":"static public void failNotEquals(":g surefire/src/main/java/org/apache/maven/surefire/battery/assertion/BatteryAssert.java

%build

%if %{with_maven}

        export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
        mkdir -p $MAVEN_REPO_LOCAL

%else
        mkdir -p lib
        build-jar-repository -s -p lib classworlds junit plexus/utils
%endif


for project in surefire surefire-booter; do

        pushd $project

                %if %{with_maven}
                        mvn-jpp \
                                -e \
                                -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
                                -Dmaven2.jpp.depmap.file=%{SOURCE4} \
                                install javadoc:javadoc
                %else

                        ant -Dmaven.mode.offline=true
                        cp -p target/*jar ../lib/$project.jar
                %endif
        popd

done

%install
rm -rf $RPM_BUILD_ROOT
# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}/maven-surefire
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/maven2/poms

for p in surefire \
        surefire-booter; do

        installname=`echo $p | sed -e s:^surefire-::g`
        install -pm 644 $p/target/$p-%{version}.jar \
          $RPM_BUILD_ROOT%{_javadir}/maven-surefire/$installname-%{version}.jar

        %add_to_maven_depmap org.apache.maven.surefire $p 1.5.3 JPP/maven-surefire $installname

        install -pm 644 $p/pom.xml \
          $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.maven-surefire-$installname.pom

done

(cd $RPM_BUILD_ROOT%{_javadir}/maven-surefire && for jar in *-%{version}*; \
  do ln -sf ${jar} `echo $jar| sed  "s|-%{version}||g"`; done)

%if %{with_maven}
# javadoc

for p in surefire \
        surefire-booter;  do

        project=`basename $p | sed -e s:surefire-::g`

        install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/maven-$p-%{version}

        cp -pr $p/target/site/apidocs/* \
          $RPM_BUILD_ROOT%{_javadocdir}/maven-$p-%{version}/

        ln -s maven-$p-%{version} $RPM_BUILD_ROOT%{_javadocdir}/maven-$p 
done

%endif

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{gcj_support}
%post

%update_maven_depmap

if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi

if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%if %{gcj_support}
%postun

%update_maven_depmap

if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%if %{gcj_support}
%post booter
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%if %{gcj_support}
%postun booter
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%files
%defattr(-,root,root,-)
%dir %{_javadir}/maven-surefire
%{_javadir}/maven-surefire/surefire*
%dir %{_datadir}/maven2
%dir %{_datadir}/maven2/poms
%{_datadir}/maven2/poms/JPP.maven-surefire-surefire.pom
%{_mavendepmapfragdir}
%{_libdir}/gcj/%{name}/booter*

%if %{gcj_support}
%dir %attr(-,root,root) %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/surefire-1.5.3.jar.*
%endif

%files booter
%defattr(-,root,root,-)
%{_javadir}/maven-surefire/booter*
%dir %{_datadir}/maven2
%dir %{_datadir}/maven2/poms
%{_datadir}/maven2/poms/JPP.maven-surefire-booter.pom

%if %{with_maven}
%if %{gcj_support}
%dir %attr(-,root,root) %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/booter-1.5.3.jar.*
%endif

%files javadoc
%defattr(-,root,root,-)
%doc %{_javadocdir}/*

%files booter-javadoc
%defattr(-,root,root,-)
%doc %{_javadocdir}/*
%endif


%changelog
* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.5.3-3.8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Aug 13 2008 Deepak Bhole <dbhole@redhat.com> 1.5.3-2.8
- Build for ppc64

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.5.3-2.7
- drop repotag

* Thu May 29 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.5.3-2jpp.6
- fix license tag

* Thu Feb 28 2008 Deepak Bhole <dbhole@redhat.com> 1.5.3-2jpp.5
- Rebuild

* Fri Sep 21 2007 Deepak Bhole <dbhole@redhat.com> 1.5.3-2jpp.4
- Build with maven
- ExcludeArch ppc64

* Fri Aug 31 2007 Deepak Bhole <dbhole@redhat.com> 0:1.5.3-2jpp.3
- Build without maven (for initial ppc build)

* Tue Mar 20 2007 Deepak Bhole <dbhole@redhat.com> 0:1.5.3-2jpp.2
- Build with maven

* Mon Feb 26 2007 Tania Bento <tbento@redhat.com> 0:1.5.3-2jpp.1
- Fixed %%Release.
- Fixed %%BuildRoot.
- Removed %%Vendor.
- Removed %%Distribution.
- Removed period at the end of %%Summary.
- Removed %%post and %%postun sections for javadoc.
- Removed %%post and %%postun sections for booter-javadoc.
- Added gcj support option.
- Fixed instructions on how to generate source drop.

* Tue Oct 17 2006 Deepak Bhole <dbhole@redhat.com> 1.5.3-2jpp
- Update for maven2 9jpp

* Mon Jun 19 2006 Deepak Bhole <dbhole@redhat.com> - 0:1.5.3-1jpp
- Initial build

