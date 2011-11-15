Name:           maven-plugin-tools
Version:        2.7
Release:        2%{?dist}
Summary:        Maven Plugin Tools

Group:          Development/Libraries
License:        ASL 2.0
URL:            http://maven.apache.org/plugin-tools/
Source0:        http://repo2.maven.org/maven2/org/apache/maven/plugin-tools/%{name}/%{version}/%{name}-%{version}-source-release.zip

# this patch should be upstreamed (together with updated pom.xml
# dependency version on jtidy 8.0)
Patch0:         0001-fix-for-new-jtidy.patch
Patch1:         0002-maven3-compat.patch

BuildArch: noarch

BuildRequires: java-devel = 1:1.6.0
BuildRequires: maven
BuildRequires: maven-install-plugin
BuildRequires: maven-compiler-plugin
BuildRequires: maven-resources-plugin
BuildRequires: maven-jar-plugin
BuildRequires: maven-source-plugin
BuildRequires: maven-plugin-plugin
BuildRequires: maven-site-plugin
BuildRequires: maven-javadoc-plugin
BuildRequires: maven-doxia-sitetools
BuildRequires: maven-doxia-tools
BuildRequires: maven-surefire-plugin
BuildRequires: maven-surefire-provider-junit
BuildRequires: maven-shared-reporting-impl
BuildRequires: maven-test-tools
BuildRequires: maven-plugin-testing-harness
BuildRequires: modello
Requires: maven
Requires:       jpackage-utils
Requires:       java

%description
The Maven Plugin Tools contains the necessary tools to be able to produce Maven Plugins in a variety of languages.

%package javadocs
Group:          Documentation
Summary:        Javadoc for %{name}
Requires:       jpackage-utils

%description javadocs
API documentation for %{name}.

%package ant
Summary: Maven Plugin Tool for Ant
Group: Development/Libraries
Requires: %{name} = %{epoch}:%{version}-%{release}
Requires: %{name}-api
Obsoletes: maven-shared-plugin-tools-ant < 0:%{version}-%{release}
Provides: maven-shared-plugin-tools-ant = 0:%{version}-%{release}

%description ant
Descriptor extractor for plugins written in Ant.

%package api
Summary: Maven Plugin Tools APIs
Group: Development/Libraries
Requires: %{name} = %{epoch}:%{version}-%{release}
Obsoletes: maven-shared-plugin-tools-api < 0:%{version}-%{release}
Provides: maven-shared-plugin-tools-api = 0:%{version}-%{release}

%description api
The Maven Plugin Tools API provides an API to extract information from
and generate documentation for Maven Plugins.

%package beanshell
Summary: Maven Plugin Tool for Beanshell
Group: Development/Libraries
Requires: %{name} = %{epoch}:%{version}-%{release}
Requires: %{name}-api
Requires: bsh
Obsoletes: maven-shared-plugin-tools-beanshell < 0:%{version}-%{release}
Provides: maven-shared-plugin-tools-beanshell = 0:%{version}-%{release}

%description beanshell
Descriptor extractor for plugins written in Beanshell.

%package java
Summary: Maven Plugin Tool for Java
Group: Development/Libraries
Requires: %{name} = %{epoch}:%{version}-%{release}
Requires: %{name}-api
Obsoletes: maven-shared-plugin-tools-java < 0:%{version}-%{release}
Provides: maven-shared-plugin-tools-java = 0:%{version}-%{release}

%description java
Descriptor extractor for plugins written in Java.

%package javadoc
Summary: Maven Plugin Tools Javadoc
Group: Development/Libraries
Requires: %{name} = %{epoch}:%{version}-%{release}
Requires: %{name}-java

%description javadoc
The Maven Plugin Tools Javadoc provides several Javadoc taglets to be used when generating Javadoc.

%package model
Summary: Maven Plugin Metadata Model
Group: Development/Libraries
Requires: %{name} = %{epoch}:%{version}-%{release}
Requires: %{name}-java
Obsoletes: maven-shared-plugin-tools-model < 0:%{version}-%{release}
Provides: maven-shared-plugin-tools-model = 0:%{version}-%{release}

%description model
The Maven Plugin Metadata Model provides an API to play with the Metadata model.

%package -n maven-plugin-plugin
Summary: Maven Plugin Plugin
Group: Development/Libraries
Requires: %{name} = %{epoch}:%{version}-%{release}
Requires: %{name}-java
Requires: %{name}-model
Requires: %{name}-beanshell
Requires: maven-doxia-sitetools
Requires: maven-shared-reporting-impl
Obsoletes: maven2-plugin-plugin < 0:%{version}-%{release}
Provides: maven2-plugin-plugin = 0:%{version}-%{release}

%description -n maven-plugin-plugin
The Plugin Plugin is used to create a Maven plugin descriptor for any Mojo's found in the source tree,
to include in the JAR. It is also used to generate Xdoc files for the Mojos as well as for updating the
plugin registry, the artifact metadata and a generic help goal.

%prep
%setup -q
%patch0
%patch1 -p1

%build
export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mvn-rpmbuild package javadoc:aggregate

%install
# jars
install -d -m 755 %{buildroot}%{_javadir}/%{name}

install -pm 644 maven-plugin-tools-ant/target/maven-plugin-tools-ant-%{version}.jar \
                %{buildroot}%{_javadir}/maven-plugin-tools/ant.jar
install -pm 644 maven-plugin-tools-api/target/maven-plugin-tools-api-%{version}.jar \
                %{buildroot}%{_javadir}/maven-plugin-tools/api.jar
install -pm 644 maven-plugin-tools-beanshell/target/maven-plugin-tools-beanshell-%{version}.jar \
                %{buildroot}%{_javadir}/maven-plugin-tools/beanshell.jar
install -pm 644 maven-plugin-tools-java/target/maven-plugin-tools-java-%{version}.jar \
                %{buildroot}%{_javadir}/maven-plugin-tools/java.jar
install -pm 644 maven-plugin-tools-javadoc/target/maven-plugin-tools-javadoc-%{version}.jar \
                %{buildroot}%{_javadir}/maven-plugin-tools/javadoc.jar
install -pm 644 maven-plugin-tools-model/target/maven-plugin-tools-model-%{version}.jar \
                %{buildroot}%{_javadir}/maven-plugin-tools/model.jar
install -pm 644 maven-plugin-plugin/target/maven-plugin-plugin-%{version}.jar \
                %{buildroot}%{_javadir}/maven-plugin-tools/plugin.jar

# pom
install -d -m 755 %{buildroot}%{_mavenpomdir}

install -pm 644 pom.xml \
                %{buildroot}%{_mavenpomdir}/JPP.%{name}-%{name}.pom
%add_maven_depmap JPP.%{name}-%{name}.pom

install -pm 644 %{name}-ant/pom.xml \
                %{buildroot}%{_mavenpomdir}/JPP.%{name}-ant.pom
%add_maven_depmap -f ant JPP.%{name}-ant.pom %{name}/ant.jar

install -pm 644 %{name}-api/pom.xml \
                %{buildroot}%{_mavenpomdir}/JPP.%{name}-api.pom
%add_maven_depmap -f api JPP.%{name}-api.pom %{name}/api.jar

install -pm 644 %{name}-beanshell/pom.xml \
                %{buildroot}%{_mavenpomdir}/JPP.%{name}-beanshell.pom
%add_maven_depmap -f beanshell JPP.%{name}-beanshell.pom %{name}/beanshell.jar

install -pm 644 %{name}-java/pom.xml \
                %{buildroot}%{_mavenpomdir}/JPP.%{name}-java.pom
%add_maven_depmap -f java JPP.%{name}-java.pom %{name}/java.jar

install -pm 644 %{name}-javadoc/pom.xml \
                %{buildroot}%{_mavenpomdir}/JPP.%{name}-javadoc.pom
%add_maven_depmap -f javadoc JPP.%{name}-javadoc.pom %{name}/javadoc.jar

install -pm 644 %{name}-model/pom.xml \
                %{buildroot}%{_mavenpomdir}/JPP.%{name}-model.pom
%add_maven_depmap -f model JPP.%{name}-model.pom %{name}/model.jar

install -pm 644 maven-plugin-plugin/pom.xml \
                %{buildroot}%{_mavenpomdir}/JPP.%{name}-plugin.pom
%add_maven_depmap -f plugin JPP.%{name}-plugin.pom %{name}/plugin.jar
# add_maven_depmap macro supports name suffixes only, renaming ...
mv -f %{buildroot}%{_mavendepmapfragdir}/%{name}-plugin %{buildroot}%{_mavendepmapfragdir}/maven-plugin-plugin

# javadoc
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}

cp -pr target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}/

%pre javadoc
# workaround for rpm bug, can be removed in F-17
[ $1 -gt 1 ] && [ -L %{_javadocdir}/%{name} ] && \
rm -rf $(readlink -f %{_javadocdir}/%{name}) %{_javadocdir}/%{name} || :

%files
%{_mavenpomdir}/JPP.%{name}-%{name}.pom
%{_mavendepmapfragdir}/%{name}

%files javadocs
%{_javadocdir}/%{name}

%files ant
%{_javadir}/%{name}/ant.jar
%{_mavenpomdir}/JPP.%{name}-ant.pom
%{_mavendepmapfragdir}/%{name}-ant

%files api
%{_javadir}/%{name}/api.jar
%{_mavenpomdir}/JPP.%{name}-api.pom
%{_mavendepmapfragdir}/%{name}-api

%files beanshell
%{_javadir}/%{name}/beanshell.jar
%{_mavenpomdir}/JPP.%{name}-beanshell.pom
%{_mavendepmapfragdir}/%{name}-beanshell

%files java
%{_javadir}/%{name}/java.jar
%{_mavenpomdir}/JPP.%{name}-java.pom
%{_mavendepmapfragdir}/%{name}-java

%files javadoc
%{_javadir}/%{name}/javadoc.jar
%{_mavenpomdir}/JPP.%{name}-javadoc.pom
%{_mavendepmapfragdir}/%{name}-javadoc

%files model
%{_javadir}/%{name}/model.jar
%{_mavenpomdir}/JPP.%{name}-model.pom
%{_mavendepmapfragdir}/%{name}-model

%files -n maven-plugin-plugin
%{_javadir}/%{name}/plugin*
%{_mavenpomdir}/JPP.%{name}-plugin.pom
%{_mavendepmapfragdir}/maven-plugin-plugin

%changelog
* Tue Aug 16 2011 Jaromir Capik <jcapik@redhat.com> -  2.7-2
- Removal of plexus-maven-plugin (not needed)
- Migration to maven3
- Removal of unwanted file duplicates
- Minor spec file changes according to the latest guidelines

* Sat Feb 12 2011 Alexander Kurtakov <akurtako@redhat.com> 0:2.7-1
- Update to new upstream release.
- Adapt to current guidelines.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Sep 30 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:2.6-8
- Remove jtidy depmap (not needed anymore)

* Wed Sep 29 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:2.6-7
- Add patch for new jtidy
- Add jtidy depmap

* Wed Sep 8 2010 Alexander Kurtakov <akurtako@redhat.com> 0:2.6-6
- BR maven-site-plugin.
- Use javadoc:aggregate for multimodule projects.

* Thu May 27 2010 Alexander Kurtakov <akurtako@redhat.com> 0:2.6-5
- Add missing requires.
- Drop modello patches not needed anymore.

* Wed May 19 2010 Alexander Kurtakov <akurtako@redhat.com> 0:2.6-4
- Fix plugin-tools-java obsoletes.

* Tue May 18 2010 Alexander Kurtakov <akurtako@redhat.com> 0:2.6-3
- More BRs.

* Tue May 18 2010 Alexander Kurtakov <akurtako@redhat.com> 0:2.6-2
- Fix BRs.

* Tue May 18 2010 Alexander Kurtakov <akurtako@redhat.com> 2.6-0
- Update to 2.6.
- Separate modules as subpackages.

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
