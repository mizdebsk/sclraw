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

# If you don't want to build with maven, and use straight ant instead,
# give rpmbuild option '--without maven'
%define with_maven 1
%define with_junit4 1
%define without_junit4 0

Name:           maven-surefire
Version:        2.3
Release:        7.5%{?dist}
Epoch:          0
Summary:        Test framework project
License:        Apache Software License
Group:          Development/Java
URL:            http://maven.apache.org/surefire/

# svn export
#    http://svn.apache.org/repos/asf/maven/surefire/tags/surefire-2.3 maven-surefire
# tar czf surefire-2.3-tar.gz maven-surefire/
Source0:        %{name}-%{version}-src.tar.gz
#Source1:        %{name}-settings.xml
Source2:        %{name}-build.xml
Source3:        %{name}-booter-build.xml
Source4:        %{name}-jpp-depmap.xml

Patch0:         %{name}-plexus12.patch
Patch1:         %{name}-buildonlyjunit3.patch
Patch2:         maven-surefire-buildskiptestng.patch
Patch3:         maven-surefire-2.3-junit4-pom.patch


BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  ant
BuildRequires:  ant-nodeps
BuildRequires:  classworlds
BuildRequires:  jpackage-utils >= 0:1.7.2
BuildRequires:  junit >= 3.8.2
BuildRequires:  plexus-utils
%if %{with_junit4}
BuildRequires:  junit4
#BuildRequires:  testng
%endif

%if %{with_maven}
BuildRequires:  maven2 >= 2.0.4
#BuildRequires:  maven2-common-poms
BuildRequires:  maven2-plugin-compiler
BuildRequires:  maven2-plugin-install
BuildRequires:  maven2-plugin-jar
BuildRequires:  maven2-plugin-javadoc
BuildRequires:  maven2-plugin-resources
BuildRequires:	maven2-plugin-site
BuildRequires:  maven2-plugin-plugin
BuildRequires:  plexus-containers-component-api >= 1.0-0.a34
BuildRequires:  tomcat5
BuildRequires:  tomcat5-servlet-2.4-api
#BuildRequires:  excalibur-avalon-logkit
#BuildRequires:  excalibur-avalon-framework
BuildRequires:  maven-shared-plugin-testing-harness
BuildRequires:  maven2-plugin-surefire < 2.3.1
BuildRequires:  bsf
%endif

Requires:       classworlds
Requires:       maven2
Requires:       junit
Requires:       plexus-utils

Requires(post):    jpackage-utils >= 0:1.7.2
Requires(postun):  jpackage-utils >= 0:1.7.2

Obsoletes:      maven-surefire-booter <= 0:1.5.3
Provides:       maven-surefire-booter = %{epoch}:%{version}-%{release}

%description
Surefire is a test framework project.

%package maven-plugin
Summary:                Surefire plugin for maven
Group:                  Development/Java
Requires:               maven-surefire = %{epoch}:%{version}-%{release}
Obsoletes:              maven2-plugin-surefire <= 0:2.0.4
Provides :              maven2-plugin-surefire = %{epoch}:%{version}-%{release}

%description maven-plugin
Maven surefire plugin for running tests via the surefire framework.

%package report-maven-plugin
Summary:                Surefire reports plugin for maven
Group:                  Development/Java
Requires:               maven-surefire = %{epoch}:%{version}-%{release}
Obsoletes:              maven2-plugin-surefire-report <= 0:2.0.4
Provides :              maven2-plugin-surefire-report = %{epoch}:%{version}-%{release}

%description report-maven-plugin
Plugin for generating reports from surefire test runs.

%package provider-junit
Summary:                JUnit3 provider for Maven Surefire
Group:                  Development/Java
Requires:               maven-surefire = %{epoch}:%{version}-%{release}
Obsoletes:              maven2-plugin-surefire-report <= 0:2.0.4O
#Obsoletes:              maven-surefire-junit = 2.3.1
Provides:              maven2-plugin-surefire-report = %{epoch}:%{version}-%{release}
#Provides:              maven-surefire-junit = 2.3.1

%description provider-junit
JUnit3 provider for Maven Surefire.

%if %with junit4
%package provider-junit4
Summary:                JUnit4 provider for Maven Surefire
Group:                  Development/Java
Requires:               maven-surefire = %{epoch}:%{version}-%{release}

%description provider-junit4
JUnit4 provider for Maven Surefire.
%endif


%package javadoc
Summary:          Javadoc for %{name}
Group:            Development/Documentation
Requires(post):   /bin/rm,/bin/ln
Requires(postun): /bin/rm

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -n %{name}

#find / -name JPP.maven2-parent.pom

#sed -i "s|<version>5</version>|<version>1</version>|" pom.xml
#sed -i "s|<relativePath>../pom/maven/pom.xml</relativePath>||" pom.xml
#rpm -ql maven2-common-poms

#cat /etc/maven/maven2-versionless-depmap.xml



# We use plexus 1.2. Delete deprecated files accordingly.
rm -f surefire-booter/src/main/java/org/apache/maven/surefire/booter/shell/CommandShell.java
rm -f surefire-booter/src/main/java/org/apache/maven/surefire/booter/shell/Shell.java
rm -f surefire-booter/src/main/java/org/apache/maven/surefire/booter/shell/CmdShell.java
rm -f surefire-booter/src/main/java/org/apache/maven/surefire/booter/Commandline.java

%patch0 -b .sav
%patch2 -b .sav
%if %{without_junit4}
%patch1 -b .sav
%endif

# Replace doxia package names
for i in maven-surefire-report-plugin/src/main/java/org/apache/maven/plugins/surefire/report/SurefireReportGenerator.java \
         maven-surefire-report-plugin/src/main/java/org/apache/maven/plugins/surefire/report/SurefireReportMojo.java; do

    sed -i -e s:org.codehaus.doxia.sink.Sink:org.apache.maven.doxia.sink.Sink:g $i
    sed -i -e s:org.codehaus.doxia.site.renderer.SiteRenderer:org.apache.maven.doxia.siterenderer.Renderer:g $i
    sed -i -r -e s:\(\\s+\)SiteRenderer\(\\s+\):\\1Renderer\\2:g $i
done

%build

%if %{with_maven}

        export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
        mkdir -p $MAVEN_REPO_LOCAL

%else
        mkdir -p lib
        build-jar-repository -s -p lib classworlds junit plexus/utils
%endif


%if %{with_maven}

cat %{SOURCE4}

    mvn-jpp \
        -e \
        -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
        -Dmaven2.jpp.depmap.file=%{SOURCE4} \
        -Dmaven.test.skip=true \
        install
#        -s %{SOURCE1} \

    for dir in maven-surefire-plugin \
               maven-surefire-report-plugin \
               surefire-api \
               surefire-booter \
               surefire-providers/surefire-junit; do
        (cd $dir
          mvn-jpp \
              -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
              -Dmaven2.jpp.depmap.file=%{SOURCE4} \
              javadoc:javadoc
        )
    done


%else
    ant -Dmaven.mode.offline=true
    cp -p target/*jar ../lib/$project.jar
%endif

%install
rm -rf $RPM_BUILD_ROOT
# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}/maven-surefire
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/maven2/poms

install -pm 644 maven-surefire-plugin/target/maven-surefire-plugin-*.jar $RPM_BUILD_ROOT%{_javadir}/maven-surefire/maven-plugin-%{version}.jar
%add_to_maven_depmap org.apache.maven.surefire maven-surefire-plugin 2.3 JPP/maven-surefire maven-plugin
install -pm 644 maven-surefire-plugin/pom.xml $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.maven-surefire-maven-plugin.pom
install -pm 644 maven-surefire-plugin/pom.xml $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.maven2.plugins-surefire-plugin.pom

install -pm 644 maven-surefire-report-plugin/target/maven-surefire-report-plugin-*.jar $RPM_BUILD_ROOT%{_javadir}/maven-surefire/report-maven-plugin-%{version}.jar
%add_to_maven_depmap org.apache.maven.surefire maven-surefire-report-plugin 2.3 JPP/maven-surefire report-maven-plugin
install -pm 644 maven-surefire-report-plugin/pom.xml $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.maven-surefire-report-maven-plugin.pom

install -pm 644 surefire-api/target/surefire-api-*.jar $RPM_BUILD_ROOT%{_javadir}/maven-surefire/api-%{version}.jar
%add_to_maven_depmap org.apache.maven.surefire surefire-api 2.3 JPP/maven-surefire api
install -pm 644 surefire-api/pom.xml $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.maven-surefire-api.pom

install -pm 644 surefire-booter/target/surefire-booter-*.jar $RPM_BUILD_ROOT%{_javadir}/maven-surefire/booter-%{version}.jar
%add_to_maven_depmap org.apache.maven.surefire surefire-booter 2.3 JPP/maven-surefire booter
install -pm 644 surefire-booter/pom.xml $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.maven-surefire-booter.pom

install -pm 644 surefire-providers/surefire-junit/target/surefire-junit-*.jar $RPM_BUILD_ROOT%{_javadir}/maven-surefire/junit-%{version}.jar
%add_to_maven_depmap org.apache.maven.surefire surefire-junit 2.3 JPP/maven-surefire junit
install -pm 644 surefire-providers/surefire-junit/pom.xml $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.maven-surefire-junit.pom

%if %{with_junit4}
install -pm 644 surefire-providers/surefire-junit4/target/surefire-junit4-*.jar $RPM_BUILD_ROOT%{_javadir}/maven-surefire/junit4-%{version}.jar
%add_to_maven_depmap org.apache.maven.surefire surefire-junit4 2.3 JPP/maven-surefire junit4
install -pm 644 surefire-providers/surefire-junit4/pom.xml $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.maven-surefire-junit4.pom
%endif

%add_to_maven_depmap org.apache.maven.surefire providers 2.3 JPP/maven-surefire providers
install -pm 644 surefire-providers/pom.xml $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.maven-surefire-providers.pom

(cd $RPM_BUILD_ROOT%{_javadir}/maven-surefire && for jar in *-%{version}*; \
  do ln -sf ${jar} `echo $jar| sed  "s|-%{version}||g"`; done)

%if %{with_maven}
# javadoc

install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/maven-surefire
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/maven-surefire/maven-plugin
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/maven-surefire/report-maven-plugin
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/maven-surefire/api
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/maven-surefire/booter
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/maven-surefire/junit
%if %{with_junit4}
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/maven-surefire/junit4
%endif

cp -pr maven-surefire-plugin/target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/maven-surefire/maven-plugin/
cp -pr maven-surefire-report-plugin/target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/maven-surefire/report-maven-plugin/
cp -pr surefire-api/target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/maven-surefire/api/
cp -pr surefire-booter/target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/maven-surefire/booter/
cp -pr surefire-providers/surefire-junit/target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/maven-surefire/junit/
%if %{with_junit4}
# FIXME: where are the junit4 javadocs?
#cp -pr surefire-providers/surefire-junit4/target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/maven-surefire/junit4/
%endif

%endif

# Create compatibility links
ln -s %{_javadir}/maven-surefire/api.jar \
      $RPM_BUILD_ROOT%{_javadir}/maven-surefire/surefire.jar

install -dm 755 $RPM_BUILD_ROOT%{_datadir}/maven2/plugins
ln -s %{_javadir}/maven-surefire/maven-surefire-plugin.jar \
      $RPM_BUILD_ROOT%{_datadir}/maven2/plugins/surefire-plugin.jar

ln -s %{_javadir}/maven-surefire/maven-surefire-report-plugin.jar \
      $RPM_BUILD_ROOT%{_datadir}/maven2/plugins/surefire-report-plugin.jar

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_maven_depmap

%postun
%update_maven_depmap

%files
%defattr(-,root,root,-)
%dir %{_javadir}/maven-surefire
%{_javadir}/maven-surefire/api*
%{_javadir}/maven-surefire/booter*
%{_javadir}/maven-surefire/surefire.jar
%{_datadir}/maven2/poms
%{_mavendepmapfragdir}

%files maven-plugin
%{_javadir}/maven-surefire/maven-plugin*
%dir %{_datadir}/maven2/plugins
%{_datadir}/maven2/plugins/surefire-plugin.jar

%files report-maven-plugin
%{_javadir}/maven-surefire/report-maven-plugin*
%dir %{_datadir}/maven2/plugins
%{_datadir}/maven2/plugins/surefire-report-plugin.jar

%files provider-junit
%{_javadir}/maven-surefire/junit[^4]*

%if %{with_junit4}
%files provider-junit4
%{_javadir}/maven-surefire/junit4*
%endif

%files javadoc
%defattr(-,root,root,-)
%doc %{_javadocdir}/*

%changelog
* Mon Aug 31 2009 Alexander Kurtakov <akurtako@redhat.com> 0:2.3-7.5
- Revert previous change.

* Mon Aug 31 2009 Alexander Kurtakov <akurtako@redhat.com> 0:2.3-7.4
- Disable not needed BRs.

* Mon Aug 31 2009 Alexander Kurtakov <akurtako@redhat.com> 0:2.3-7.3
- Install JPP.maven2.plugins-surefire-plugin.pom now that we have maven 2.0.8.

* Wed Aug 19 2009 Alexander Kurtakov <akurtako@redhat.com> 0:2.3-7.2
- Don't install JPP.maven2.plugins-surefire-plugin.pom to fix conflict with maven2 2.0.4.

* Tue Aug 18 2009 Alexander Kurtakov <akurtako@redhat.com> 0:2.3-7.1
- Update to 2.3 - sync with jpackage.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.5.3-4.8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

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
