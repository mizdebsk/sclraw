
%global with_maven 1

%global parent plexus
%global subname containers

# this needs to be exact version of maven-javadoc-plugin for
# integration tests
%global javadoc_plugin_version 2.7

Name:           %{parent}-%{subname}
Version:        1.5.5
Release:        2%{?dist}
Summary:        Containers for Plexus
License:        ASL 2.0 and Plexus
Group:          Development/Libraries
URL:            http://plexus.codehaus.org/
# svn export \
#  http://svn.codehaus.org/plexus/plexus-containers/tags/plexus-containers-1.5.5
# tar caf plexus-containers-1.5.5.tar.xz plexus-containers-1.5.5
Source0:        %{name}-%{version}.tar.xz
Source1:        plexus-container-default-build.xml
Source2:        plexus-component-annotations-build.xml
Source3:        plexus-containers-settings.xml

Patch0:         plexus-containers-test-oom.patch


BuildArch:      noarch

BuildRequires:  jpackage-utils >= 0:1.7.3
%if %{with_maven}
BuildRequires:  maven
BuildRequires:  maven-compiler-plugin
BuildRequires:  maven-install-plugin
BuildRequires:  maven-invoker-plugin
BuildRequires:  maven-jar-plugin
BuildRequires:  maven-javadoc-plugin = %{javadoc_plugin_version}
BuildRequires:  maven-resources-plugin
BuildRequires:  maven-site-plugin
BuildRequires:  maven-shared-invoker
BuildRequires:  maven-surefire-maven-plugin
BuildRequires:  maven-surefire-provider-junit
BuildRequires:  maven-doxia
BuildRequires:  maven-doxia-sitetools
BuildRequires:  maven2-common-poms >= 1.0
BuildRequires:  maven-release
BuildRequires:  maven-plugin-plugin
%else
BuildRequires:  ant >= 0:1.6.5
BuildRequires:  ant-junit
BuildRequires:  junit
%endif
BuildRequires:  plexus-classworlds
BuildRequires:  plexus-utils
BuildRequires:  plexus-cli
BuildRequires:  xbean
BuildRequires:  guava

Requires:       plexus-classworlds >= 2.2.3
Requires:       plexus-utils
Requires:       xbean
Requires:       guava

Requires(post):    jpackage-utils >= 0:1.7.2
Requires(postun):  jpackage-utils >= 0:1.7.2

%description
The Plexus project seeks to create end-to-end developer tools for
writing applications. At the core is the container, which can be
embedded or for a full scale application server. There are many
reusable components for hibernate, form processing, jndi, i18n,
velocity, etc. Plexus also includes an application server which
is like a J2EE application server, without all the baggage.

%package component-metadata
Summary:        Component metadata from %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       plexus-cli

%description component-metadata
%{summary}.

%package component-javadoc
Summary:        Javadoc component from %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description component-javadoc
%{summary}.


%package component-annotations
Summary:        Component API from %{name}
Group:          Documentation
Requires:       %{name} = %{version}-%{release}

%description component-annotations
%{summary}.

%package container-default
Summary:        Default Container from %{name}
Group:          Development/Libraries
Requires:       %{name}-component-annotations = %{version}-%{release}
Provides:       plexus-containers-component-api = %{version}-%{release}

%description container-default
%{summary}.

%package javadoc
Summary:        API documentation for all plexus-containers packages
Group:          Documentation
Requires:       jpackage-utils
Provides:       %{name}-component-annotations-javadoc = %{version}-%{release}
Obsoletes:      %{name}-component-annotations-javadoc < %{version}-%{release}
Provides:       %{name}-component-javadoc-javadoc = %{version}-%{release}
Obsoletes:      %{name}-component-javadoc-javadoc < %{version}-%{release}
Provides:       %{name}-component-metadata-javadoc = %{version}-%{release}
Obsoletes:      %{name}-component-metadata-javadoc < %{version}-%{release}
Provides:       %{name}-container-default-javadoc = %{version}-%{release}
Obsoletes:      %{name}-container-default-javadoc < %{version}-%{release}

%description javadoc
%{summary}.

%prep
%setup -q -n plexus-containers-%{version}

cp %{SOURCE1} plexus-container-default/build.xml
cp %{SOURCE2} plexus-component-annotations/build.xml

%patch0

# to prevent ant from failing
mkdir -p plexus-component-annotations/src/test/java

# integration tests fix
sed -i "s|<version>2.3</version>|<version> %{javadoc_plugin_version}</version>|" plexus-component-javadoc/src/it/basic/pom.xml

%build

%if %{with_maven}
    mvn-rpmbuild -Dmaven.test.skip=true install

    # for integration tests ran during javadoc:javadoc
    for file in $MAVEN_REPO_LOCAL/org/apache/maven/plugins/maven-javadoc-plugin/%{javadoc_plugin_version}/*;do
        sha1sum $file | awk '{print $1}' > $ile.sha1
    done

    mvn-rpmbuild javadoc:aggregate
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
CLASSPATH=$CLASSPATH:../plexus-component-annotations/target/plexus-component-annotations-%{version}.jar
CLASSPATH=$CLASSPATH:target/classes:target/test-classes
ant -Dbuild.sysclasspath=only jar javadoc
popd
%endif

%install
# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}/plexus
install -pm 644 plexus-container-default/target/*.jar \
 $RPM_BUILD_ROOT%{_javadir}/%{parent}/containers-container-default.jar
install -pm 644 plexus-component-annotations/target/*.jar \
 $RPM_BUILD_ROOT%{_javadir}/%{parent}/containers-component-annotations.jar
install -pm 644 plexus-component-metadata/target/*.jar \
 $RPM_BUILD_ROOT%{_javadir}/%{parent}/containers-component-metadata.jar
install -pm 644 plexus-component-annotations/target/*.jar \
 $RPM_BUILD_ROOT%{_javadir}/%{parent}/containers-component-javadoc.jar

# pom
install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -pm 644 \
 pom.xml $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{parent}-%{subname}.pom
install -pm 644 \
 plexus-container-default/pom.xml \
 $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{name}-container-default.pom
install -pm 644 \
 plexus-component-annotations/pom.xml \
 $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{name}-component-annotations.pom
install -pm 644 \
 plexus-component-metadata/pom.xml \
 $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{name}-component-metadata.pom
install -pm 644 \
 plexus-component-javadoc/pom.xml \
 $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{name}-component-javadoc.pom

%add_to_maven_depmap org.codehaus.plexus %{name} %{version} JPP/%{parent} %{subname}
%add_to_maven_depmap org.codehaus.plexus plexus-component-annotations %{version} JPP/%{parent} containers-component-annotations
%add_to_maven_depmap org.codehaus.plexus plexus-container-default %{version} JPP/%{parent} containers-container-default
%add_to_maven_depmap org.codehaus.plexus plexus-component-metadata %{version} JPP/%{parent} containers-component-metadata
%add_to_maven_depmap org.codehaus.plexus plexus-component-javadoc %%{version} JPP/%{parent} containers-component-javadoc

# component-api is now folded into container-default
%add_to_maven_depmap org.codehaus.plexus containers-component-api %{version} JPP/%{parent} containers-container-default

# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -pr target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}

%pre javadoc
# workaround for rpm bug, can be removed in F-18
[ $1 -gt 1 ] && [ -L %{_javadocdir}/%{name} ] && \
rm -rf $(readlink -f %{_javadocdir}/%{name}) %{_javadocdir}/%{name} || :


%post component-metadata
%update_maven_depmap

%postun component-metadata
%update_maven_depmap

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
%{_mavenpomdir}/*
%{_mavendepmapfragdir}/%{name}

%files component-annotations
%defattr(-,root,root,-)
%{_javadir}/%{parent}/containers-component-annotations*

%files container-default
%defattr(-,root,root,-)
%{_javadir}/%{parent}/containers-container-default*

%files component-metadata
%defattr(-,root,root,-)
%{_javadir}/%{parent}/containers-component-metadata*

%files component-javadoc
%defattr(-,root,root,-)
%{_javadir}/%{parent}/containers-component-javadoc*

%files javadoc
%defattr(-,root,root,-)
%doc %{_javadocdir}/*

%changelog
* Mon Feb 28 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.5.5-2
- Remove unneeded env var definitions

* Fri Feb 25 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.5.5-1
- Update to latest upstream
- Remove obsolete patches
- Use maven 3 to build
- Packaging fixes
- Versionless jars & javadocs

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Oct 11 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.5.4-4
- Add plexus-cli to component-metadata Requires

* Wed Sep  8 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.5.4-3
- Use javadoc:aggregate
- Merge javadoc subpackages into one -javadoc

* Thu Jul 15 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.5.4-2
- Fix maven depmaps

* Tue Jul 13 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.5.4-1
- Version bump
- Add new sub-packages
- Cleanups

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
