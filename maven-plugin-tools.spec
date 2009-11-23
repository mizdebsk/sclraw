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

Name:           maven-plugin-tools
Version:        2.1
Release:        6%{?dist}
Epoch:          0
Summary:        Maven Plugin Tools
License:        ASL 2.0
Group:          Development/Libraries
URL:            http://maven.apache.org/plugin-tools/
Source0:        %{name}-%{version}-src.tar.gz
# svn export https://svn.apache.org/repos/asf/maven/shared/tags/maven-plugin-tools-2.1
# tar czf maven-plugin-tools-2.1-src.tar.gz maven-plugin-tools-2.1

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:    jpackage-utils >= 0:1.7.2
BuildRequires:    maven2 >= 2.0.4-9
BuildRequires:    maven2-plugin-compiler
BuildRequires:    maven2-plugin-install
BuildRequires:    maven2-plugin-jar
BuildRequires:    maven2-plugin-javadoc
BuildRequires:    maven2-plugin-resources
BuildRequires:    maven2-plugin-surefire = 2.3
BuildRequires:    maven-surefire-provider-junit = 2.3
BuildRequires:    maven2-common-poms >= 1.0-2
BuildRequires:    maven-doxia
BuildRequires:    maven-doxia-sitetools
BuildRequires:    classworlds
BuildRequires:    plexus-container-default
BuildRequires:    plexus-utils >= 1.4.5
BuildRequires:    java-devel

BuildRequires:  tomcat5
BuildRequires:  tomcat5-servlet-2.4-api

Requires(post):    jpackage-utils >= 0:1.7.2
Requires(postun):  jpackage-utils >= 0:1.7.2

%description
The Maven Plugin Tools contains the necessary tools to play with Maven Plugins.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Documentation

%description javadoc
Java API documentation for %{name}.

%prep
%setup -q -n %{name}-%{version}

%build

export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mkdir -p $MAVEN_REPO_LOCAL

mvn-jpp \
    -e \
    -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
    install

# Manual iteration should not be needed, but there is a bug in the javadoc
# plugin which makes this necessary. See:
# http://jira.codehaus.org/browse/MJAVADOC-157
for dir in %{name}-*; do
    pushd $dir >& /dev/null
        mvn-jpp \
            -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
            javadoc:javadoc
    popd >& /dev/null
done

%install
rm -rf $RPM_BUILD_ROOT
# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}/%{name}

install -pm 644 maven-plugin-tools-ant/target/maven-plugin-tools-ant-%{version}.jar \
                $RPM_BUILD_ROOT%{_javadir}/maven-plugin-tools/ant-%{version}.jar
install -pm 644 maven-plugin-tools-api/target/maven-plugin-tools-api-%{version}.jar \
                $RPM_BUILD_ROOT%{_javadir}/maven-plugin-tools/api-%{version}.jar
install -pm 644 maven-plugin-tools-beanshell/target/maven-plugin-tools-beanshell-%{version}.jar \
                $RPM_BUILD_ROOT%{_javadir}/maven-plugin-tools/beanshell-%{version}.jar
install -pm 644 maven-plugin-tools-java/target/maven-plugin-tools-java-%{version}.jar \
                $RPM_BUILD_ROOT%{_javadir}/maven-plugin-tools/java-%{version}.jar
install -pm 644 maven-plugin-tools-model/target/maven-plugin-tools-model-%{version}.jar \
                $RPM_BUILD_ROOT%{_javadir}/maven-plugin-tools/model-%{version}.jar

(cd $RPM_BUILD_ROOT%{_javadir}/%{name} && for jar in *-%{version}*; \
  do ln -sf ${jar} `echo $jar| sed  "s|-%{version}||g"`; done)

# pom
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/maven2/poms

install -pm 644 pom.xml \
                $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{name}-%{name}.pom
%add_to_maven_depmap org.apache.maven %{name} %{version} JPP/%{name} %{name}

install -pm 644 maven-plugin-tools-ant/pom.xml \
                $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{name}-ant.pom
%add_to_maven_depmap org.apache.maven %{name}-ant %{version} JPP/%{name} ant

install -pm 644 maven-plugin-tools-api/pom.xml \
                $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{name}-api.pom
%add_to_maven_depmap org.apache.maven %{name}-api %{version} JPP/%{name} api

install -pm 644 maven-plugin-tools-beanshell/pom.xml \
                $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{name}-beanshell.pom
%add_to_maven_depmap org.apache.maven %{name}-beanshell %{version} JPP/%{name} beanshell

install -pm 644 maven-plugin-tools-java/pom.xml \
                $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{name}-java.pom
%add_to_maven_depmap org.apache.maven %{name}-java %{version} JPP/%{name} java

install -pm 644 maven-plugin-tools-model/pom.xml \
                $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{name}-model.pom
%add_to_maven_depmap org.apache.maven %{name}-model %{version} JPP/%{name} model

# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}

for dir in %{name}-*; do
    install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/$dir
    cp -pr $dir/target/site/apidocs/* \
        $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/$dir/
done

ln -s %{name}-%{version} \
     $RPM_BUILD_ROOT%{_javadocdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_maven_depmap

%postun
%update_maven_depmap

%files
%defattr(-,root,root,-)
%{_javadir}/%{name}
%{_datadir}/maven2
%{_mavendepmapfragdir}

%files javadoc
%defattr(-,root,root,-)
%doc %{_javadocdir}/*

%changelog
* Mon Nov 23 2009 Alexander Kurtakov <akurtako@redhat.com> 0:2.1-6
- BR maven-plugin-tools.

* Mon Aug 31 2009 Alexander Kurtakov <akurtako@redhat.com> 0:2.1-5
- Set minimum version for plexus-utils BR.
- BR java-devel.
- Fix javadoc subpackage description.

* Mon Aug 31 2009 Alexander Kurtakov <akurtako@redhat.com> 0:2.1-4
- Adapt for Fedora.

* Wed May 20 2009 Fernando Nasser <fnasser@redhat.com> - 0:2.1-3
- Fix license
- Fix URL

* Mon Apr 27 2009 Yong Yang <yyang@redhat.com> - 0:2.1-2
- Add BRs for maven-doxia*
- Rebuild with maven2-2.0.8 built in non-bootstrap mode

* Mon Mar 09 2009 Yong Yang <yyang@redhat.com> - 0:2.1-1
- Import from dbhole's maven2 2.0.8 packages

* Mon Apr 07 2008 Deepak Bhole <dbhole@redhat.com> - 0:2.1-0jpp.1
- Initial build
