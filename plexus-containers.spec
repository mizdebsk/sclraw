# Copyright (c) 2000-2007, JPackage Project
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

%define with_maven 0

%define parent plexus
%define subname containers
%define namedversion 1.0-alpha-34

Name:           %{parent}-%{subname}
Version:        1.0
Release:        0.1.a34.7%{?dist}
Epoch:          0
Summary:        Containers for Plexus
License:        ASL 2.0 and Plexus
Group:          Development/Libraries
URL:            http://plexus.codehaus.org/
# svn export \
#  http://svn.codehaus.org/plexus/plexus-containers/tags/plexus-containers-1.0-alpha-34/
# tar czf plexus-containers-1.0-alpha-34.tar.gz plexus-containers-1.0-alpha-34/
Source0:        %{name}-%{namedversion}.tar.gz
Source1:        plexus-container-default-build.xml
Source2:        plexus-component-annotations-build.xml
Source3:        plexus-containers-settings.xml

Patch0:         plexus-containers-javadoc-junit-link.patch
Patch1:         plexus-containers-sourcetarget.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  jpackage-utils >= 0:1.7.3
%if %{with_maven}
BuildRequires:  maven2 >= 2.0.4-10jpp
BuildRequires:  maven2-plugin-compiler
BuildRequires:  maven2-plugin-install
BuildRequires:  maven2-plugin-jar
BuildRequires:  maven2-plugin-javadoc
BuildRequires:  maven2-plugin-resources
BuildRequires:  maven2-plugin-surefire = 2.3
BuildRequires:  maven-surefire-provider-junit = 2.3
BuildRequires:  maven-doxia
BuildRequires:  maven-doxia-sitetools
BuildRequires:  maven2-common-poms >= 1.0
BuildRequires:  maven-release
%else
BuildRequires:  ant >= 0:1.6.5
BuildRequires:  ant-junit
BuildRequires:  junit
%endif
BuildRequires:  plexus-classworlds
BuildRequires:  plexus-utils

Requires:       plexus-classworlds
Requires:       plexus-utils

Requires(post):    jpackage-utils >= 0:1.7.2
Requires(postun):  jpackage-utils >= 0:1.7.2

%description
The Plexus project seeks to create end-to-end developer tools for
writing applications. At the core is the container, which can be
embedded or for a full scale application server. There are many
reusable components for hibernate, form processing, jndi, i18n,
velocity, etc. Plexus also includes an application server which
is like a J2EE application server, without all the baggage.


%package component-annotations
Summary:        Component API from %{name}
Group:          Documentation
Requires:       %{name} = %{epoch}:%{version}-%{release}
Requires:       plexus-classworlds

%description component-annotations
%{summary}.

%package container-default
Summary:        Default Container from %{name}
Group:          Documentation
Requires:       %{name} = %{epoch}:%{version}-%{release}
Requires:       plexus-classworlds
Requires:       plexus-containers-component-annotations
Requires:       plexus-utils
Provides:       plexus-containers-component-api = %{epoch}:%{version}-%{release}

%description container-default
%{summary}.

%package component-annotations-javadoc
Summary:        Javadoc for plexus-component-annotations
Group:          Documentation
BuildRequires:  java-javadoc
BuildRequires:  jakarta-commons-collections-javadoc
BuildRequires:  jakarta-commons-dbcp-javadoc
BuildRequires:  jakarta-commons-fileupload-javadoc
BuildRequires:  jakarta-commons-httpclient-javadoc
BuildRequires:  jakarta-commons-logging-javadoc
BuildRequires:  jakarta-commons-pool-javadoc
BuildRequires:  log4j-javadoc
BuildRequires:  regexp-javadoc
BuildRequires:  velocity-javadoc
Requires:       java-javadoc
Requires:       jakarta-commons-collections-javadoc
Requires:       jakarta-commons-dbcp-javadoc
Requires:       jakarta-commons-fileupload-javadoc
Requires:       jakarta-commons-httpclient-javadoc
Requires:       jakarta-commons-logging-javadoc
Requires:       jakarta-commons-pool-javadoc
Requires:       log4j-javadoc
Requires:       regexp-javadoc
Requires:       velocity-javadoc

%description component-annotations-javadoc
%{summary}.

%package container-default-javadoc
Summary:        Javadoc for plexus-container-default
Group:          Documentation

%description container-default-javadoc
%{summary}.

%prep
%setup -q -n plexus-containers-%{namedversion}

cp %{SOURCE1} plexus-container-default/build.xml
cp %{SOURCE2} plexus-component-annotations/build.xml

%patch0 -b .sav0
%patch1 -b .sav0

# Remove test that fails upstream as well
rm -f \
 plexus-container-default/src/test/java/org/codehaus/plexus/logging/console/ConsoleLoggerTest.java

# to prevent ant from failing
mkdir -p plexus-component-annotations/src/test/java

%build

export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mkdir -p $MAVEN_REPO_LOCAL

# FIXME
# Why does maven not support assert: "/UriConverter.java:[33,19] ';' expected"?
sed -i "s|assert|// assert|g" \
 plexus-container-default/src/main/java/org/codehaus/plexus/component/configurator/converters/basic/UriConverter.java

%if %{with_maven}
    mvn-jpp \
        -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
        install

    # Manual iteration should not be needed, but there is a bug in the javadoc 
    # plugin which makes this necessary. See: 
    # http://jira.codehaus.org/browse/MJAVADOC-157

    for module in container-default \
                  component-annotations; do
        pushd plexus-$module
            mvn-jpp \
                -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
                 javadoc:javadoc
        popd
    done

%else
export OPT_JAR_LIST="ant/ant-junit junit"
pushd plexus-component-annotations
export CLASSPATH=$(build-classpath \
plexus/classworlds \
)
ant -Dbuild.sysclasspath=only jar javadoc
popd
pushd plexus-container-default
rm src/test/java/org/codehaus/plexus/hierarchy/PlexusHierarchyTest.java
CLASSPATH=$CLASSPATH:$(build-classpath \
plexus/utils \
)
CLASSPATH=$CLASSPATH:../plexus-component-annotations/target/plexus-component-annotations-%{namedversion}.jar
CLASSPATH=$CLASSPATH:target/classes:target/test-classes
ant -Dbuild.sysclasspath=only jar javadoc
popd
%endif

%install
rm -rf $RPM_BUILD_ROOT
# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}/plexus
install -pm 644 plexus-container-default/target/*.jar \
 $RPM_BUILD_ROOT%{_javadir}/%{parent}/containers-container-default-%{version}.jar
install -pm 644 plexus-component-annotations/target/*.jar \
 $RPM_BUILD_ROOT%{_javadir}/%{parent}/containers-component-annotations-%{version}.jar

(cd $RPM_BUILD_ROOT%{_javadir}/%{parent} && for jar in *-%{version}*; \
  do ln -sf ${jar} `echo $jar| sed  "s|-%{version}||g"`; done)

# pom
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/maven2/poms
install -pm 644 \
 pom.xml $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{parent}-%{subname}.pom
install -pm 644 \
 plexus-container-default/pom.xml \
 $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{parent}-containers-container-default.pom
install -pm 644 \
 plexus-component-annotations/pom.xml \
 $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{parent}-containers-component-annotations.pom
%add_to_maven_depmap org.codehaus.plexus %{name} %{namedversion} JPP/%{parent} %{subname}
%add_to_maven_depmap org.codehaus.plexus containers-container-default %{namedversion} JPP/%{parent} containers-container-default
%add_to_maven_depmap org.codehaus.plexus containers-component-annotations %{namedversion} JPP/%{parent} containers-component-annotations

# component-api is now folded into container-default
%add_to_maven_depmap org.codehaus.plexus containers-component-api %{namedversion} JPP/%{parent} containers-container-default

# javadoc
install -d -m 755 \
 $RPM_BUILD_ROOT%{_javadocdir}/%{parent}-containers-component-annotations-%{version}
%if %{with_maven}
cp -pr plexus-component-annotations/target/site/apidocs/* \
 $RPM_BUILD_ROOT%{_javadocdir}/%{parent}-containers-component-annotations-%{version}
%else
# directory name is annotationsdocs while building with ant
ls -l plexus-component-annotations/target/site/
cp -pr plexus-component-annotations/target/site/annotationsdocs/* \
 $RPM_BUILD_ROOT%{_javadocdir}/%{parent}-containers-component-annotations-%{version}
%endif

install -d -m 755 \
 $RPM_BUILD_ROOT%{_javadocdir}/%{parent}-containers-container-default-%{version}

cp -pr plexus-container-default/target/site/apidocs/* \
 $RPM_BUILD_ROOT%{_javadocdir}/%{parent}-containers-container-default-%{version}

ln -s %{parent}-containers-component-annotations-%{version} \
 $RPM_BUILD_ROOT%{_javadocdir}/%{parent}-containers-component-annotations
ln -s %{parent}-containers-container-default-%{version} \
 $RPM_BUILD_ROOT%{_javadocdir}/%{parent}-containers-container-default

%clean
rm -rf $RPM_BUILD_ROOT

%post component-annotations
%update_maven_depmap

%postun component-annotations
%update_maven_depmap

%post container-default
%update_maven_depmap

%postun container-default
%update_maven_depmap

%files
%defattr(-,root,root,-)
%{_datadir}/maven2/poms/*
%{_mavendepmapfragdir}

%files component-annotations
%defattr(-,root,root,-)
%{_javadir}/%{parent}/containers-component-annotations*

%files container-default
%defattr(-,root,root,-)
%{_javadir}/%{parent}/containers-container-default*

%files component-annotations-javadoc
%defattr(-,root,root,-)
%doc %{_javadocdir}/plexus-containers-component-annotations-%{version}
%doc %{_javadocdir}/plexus-containers-component-annotations

%files container-default-javadoc
%defattr(-,root,root,-)
%doc %{_javadocdir}/plexus-containers-container-default-%{version}
%doc %{_javadocdir}/plexus-containers-container-default

%changelog
* Thu Aug 20 2009 Andrew Overholt <overholt@redhat.com> 0:1.0-0.1.a34.7
- Clean up javadoc post/postun
- Build with ant
- Remove gcj support
- Clean up groups

* Fri May 15 2009 Fernando Nasser <fnasser@redhat.com> 1.0-0.1.a34.6
- Fix license

* Tue Apr 28 2009 Yong Yang <yyang@redhat.com> 1.0-0.1.a34.5
- Add BRs maven2-plugin-surfire*, maven-doxia*
- Merge from RHEL-4-EP-5 1.0-0.1.a34.2, add plexus-containers-sourcetarget.patch
- Rebuild with new maven2 2.0.8 built in non-bootstrap mode

* Mon Mar 16 2009 Yong Yang <yyang@redhat.com> 1.0-0.1.a34.4
- rebuild with new maven2 2.0.8 built in bootstrap mode

* Wed Feb 04 2009 Yong Yang <yyang@redhat.com> - 1.0-0.1.a34.3
- re-build with maven

* Wed Feb 04 2009 Yong Yang <yyang@redhat.com> - 1.0-0.1.a34.2
- fix bulding with ant
- temporarily buid with ant

* Wed Jan 14 2009 Yong Yang <yyang@redhat.com> - 1.0-0.1.a34.1jpp.2
- re-build with maven
- disabled assert in plexus-container-default/.../UriConverter.java???

* Tue Jan 13 2009 Yong Yang <yyang@redhat.com> - 1.0-0.1.a34.1jpp.1
- Imported into devel from dbhole's maven 2.0.8 packages

* Tue Apr 08 2008 Deepak Bhole <dbhole@redhat.com> 1.0-0.1.a34.0jpp.1
- Initial build with original base spec from JPackage
