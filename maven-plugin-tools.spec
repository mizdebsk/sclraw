Name:           maven-plugin-tools
Version:        2.6
Release:        5%{?dist}
Summary:        Maven Plugin Tools

Group:          Development/Libraries
License:        ASL 2.0
URL:            http://maven.apache.org/plugin-tools/
Epoch:          0
#svn export http://svn.apache.org/repos/asf/maven/plugin-tools/tags/maven-plugin-tools-2.6 maven-plugin-tools-2.6
#tar caf maven-plugin-tools-2.6.tar.xz maven-plugin-tools-2.6/
Source0:        %{name}-%{version}.tar.xz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch: noarch

BuildRequires: java-devel >= 1:1.6.0
BuildRequires: maven-install-plugin
BuildRequires: maven-compiler-plugin
BuildRequires: maven-resources-plugin
BuildRequires: maven-jar-plugin
BuildRequires: maven2-plugin-source
BuildRequires: maven-plugin-plugin
BuildRequires: plexus-maven-plugin
BuildRequires: maven-javadoc-plugin
BuildRequires: maven-doxia-sitetools
BuildRequires: maven-doxia-tools
BuildRequires: maven-surefire-maven-plugin
BuildRequires: maven-surefire-provider-junit
BuildRequires: maven-shared-reporting-impl
BuildRequires: maven-shared-test-tools
BuildRequires: maven-plugin-testing-harness
Requires: maven2
Requires:       jpackage-utils
Requires:       java
Requires(post):       jpackage-utils
Requires(postun):     jpackage-utils

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
rm -fr src/site/site.xml

%build
export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mvn-jpp \
        -e \
        -Dmaven2.jpp.mode=true \
        -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
        -Dmaven.test.skip=true \
        package javadoc:javadoc

%install
rm -rf %{buildroot}

# jars
install -d -m 755 %{buildroot}%{_javadir}/%{name}

install -pm 644 maven-plugin-tools-ant/target/maven-plugin-tools-ant-%{version}.jar \
                %{buildroot}%{_javadir}/maven-plugin-tools/ant-%{version}.jar
install -pm 644 maven-plugin-tools-api/target/maven-plugin-tools-api-%{version}.jar \
                %{buildroot}%{_javadir}/maven-plugin-tools/api-%{version}.jar
install -pm 644 maven-plugin-tools-beanshell/target/maven-plugin-tools-beanshell-%{version}.jar \
                %{buildroot}%{_javadir}/maven-plugin-tools/beanshell-%{version}.jar
install -pm 644 maven-plugin-tools-java/target/maven-plugin-tools-java-%{version}.jar \
                %{buildroot}%{_javadir}/maven-plugin-tools/java-%{version}.jar
install -pm 644 maven-plugin-tools-javadoc/target/maven-plugin-tools-javadoc-%{version}.jar \
                %{buildroot}%{_javadir}/maven-plugin-tools/javadoc-%{version}.jar
install -pm 644 maven-plugin-tools-model/target/maven-plugin-tools-model-%{version}.jar \
                %{buildroot}%{_javadir}/maven-plugin-tools/model-%{version}.jar
install -pm 644 maven-plugin-plugin/target/maven-plugin-plugin-%{version}.jar \
                %{buildroot}%{_javadir}/maven-plugin-tools/plugin-%{version}.jar

(cd $RPM_BUILD_ROOT%{_javadir}/%{name} && for jar in *-%{version}*; \
  do ln -sf ${jar} `echo $jar| sed  "s|-%{version}||g"`; done)

# pom
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/maven2/poms

install -pm 644 pom.xml \
                $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{name}-%{name}.pom
%add_to_maven_depmap org.apache.maven.plugin-tools %{name} %{version} JPP/%{name} %{name}

install -pm 644 maven-plugin-tools-ant/pom.xml \
                $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{name}-ant.pom
%add_to_maven_depmap org.apache.maven.plugin-tools %{name}-ant %{version} JPP/%{name} ant

install -pm 644 maven-plugin-tools-api/pom.xml \
                $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{name}-api.pom
%add_to_maven_depmap org.apache.maven.plugin-tools %{name}-api %{version} JPP/%{name} api

install -pm 644 maven-plugin-tools-beanshell/pom.xml \
                $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{name}-beanshell.pom
%add_to_maven_depmap org.apache.maven.plugin-tools %{name}-beanshell %{version} JPP/%{name} beanshell

install -pm 644 maven-plugin-tools-java/pom.xml \
                $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{name}-java.pom
%add_to_maven_depmap org.apache.maven.plugin-tools %{name}-java %{version} JPP/%{name} java

install -pm 644 maven-plugin-tools-javadoc/pom.xml \
                $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{name}-javadoc.pom
%add_to_maven_depmap org.apache.maven.plugin-tools %{name}-javadoc %{version} JPP/%{name} javadoc

install -pm 644 maven-plugin-tools-model/pom.xml \
                $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{name}-model.pom
%add_to_maven_depmap org.apache.maven.plugin-tools %{name}-model %{version} JPP/%{name} model

install -pm 644 maven-plugin-plugin/pom.xml \
                $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{name}-plugin.pom
%add_to_maven_depmap org.apache.maven.plugins maven-plugin-plugin %{version} JPP/%{name} plugin

# javadoc
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}-%{version}

for dir in maven-plugin-*; do
    install -d -m 755 %{buildroot}%{_javadocdir}/%{name}-%{version}/$dir
    cp -pr $dir/target/site/apidocs/* \
        %{buildroot}%{_javadocdir}/%{name}-%{version}/$dir/
done

ln -s %{name}-%{version} \
     $RPM_BUILD_ROOT%{_javadocdir}/%{name}

%post
%update_maven_depmap

%postun
%update_maven_depmap

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_javadir}/*
%{_mavenpomdir}/*
%{_mavendepmapfragdir}/*

%files javadocs
%defattr(-,root,root,-)
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}

%files ant
%defattr(-,root,root,-)
%{_javadir}/%{name}/ant*

%files api
%defattr(-,root,root,-)
%{_javadir}/%{name}/api*

%files beanshell
%defattr(-,root,root,-)
%{_javadir}/%{name}/beanshell*

%files java
%defattr(-,root,root,-)
%{_javadir}/%{name}/java.*
%{_javadir}/%{name}/java-*

%files javadoc
%defattr(-,root,root,-)
%{_javadir}/%{name}/javadoc*

%files model
%defattr(-,root,root,-)
%{_javadir}/%{name}/model*

%files -n maven-plugin-plugin
%defattr(-,root,root,-)
%{_javadir}/%{name}/plugin*

%changelog
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
