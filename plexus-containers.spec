
%global with_maven 1

%global parent plexus
%global subname containers

# this needs to be exact version of maven-javadoc-plugin for
# integration tests
%global javadoc_plugin_version 2.9

Name:           %{parent}-%{subname}
Version:        1.5.5
Release:        7%{?dist}
Summary:        Containers for Plexus
License:        ASL 2.0 and MIT
Group:          Development/Libraries
URL:            http://plexus.codehaus.org/
# svn export \
#  http://svn.codehaus.org/plexus/plexus-containers/tags/plexus-containers-1.5.5
# tar caf plexus-containers-1.5.5.tar.xz plexus-containers-1.5.5
Source0:        %{name}-%{version}.tar.xz
Source1:        plexus-container-default-build.xml
Source2:        plexus-component-annotations-build.xml
Source3:        plexus-containers-settings.xml

Patch0:         0001-Fix-test-oom.patch
Patch1:         0002-Fix-maven3-compatibility.patch
Patch2:         0003-Fix-OpenJDK7-compatibility.patch

BuildArch:      noarch

BuildRequires:  jpackage-utils >= 0:1.7.3
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
BuildRequires:  maven-release
BuildRequires:  maven-plugin-plugin
BuildRequires:  plexus-classworlds
BuildRequires:  plexus-utils
BuildRequires:  plexus-cli
BuildRequires:  xbean
BuildRequires:  guava

Requires:       plexus-classworlds >= 2.2.3
Requires:       plexus-utils
Requires:       xbean
Requires:       guava


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

%patch0 -p1
%patch1 -p1
%patch2 -p1

# to prevent ant from failing
mkdir -p plexus-component-annotations/src/test/java

# integration tests fix
sed -i "s|<version>2.3</version>|<version> %{javadoc_plugin_version}</version>|" plexus-component-javadoc/src/it/basic/pom.xml

%build

mvn-rpmbuild -Dmaven.test.skip=true install

# for integration tests ran during javadoc:javadoc
for file in $MAVEN_REPO_LOCAL/org/apache/maven/plugins/maven-javadoc-plugin/%{javadoc_plugin_version}/*;do
    sha1sum $file | awk '{print $1}' > $ile.sha1
done

mvn-rpmbuild javadoc:aggregate

%install
# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}/plexus
install -pm 644 plexus-component-annotations/target/*.jar \
 $RPM_BUILD_ROOT%{_javadir}/%{parent}/%{subname}-component-annotations.jar
install -pm 644 plexus-container-default/target/*.jar \
 $RPM_BUILD_ROOT%{_javadir}/%{parent}/%{subname}-container-default.jar
install -pm 644 plexus-component-metadata/target/*.jar \
 $RPM_BUILD_ROOT%{_javadir}/%{parent}/%{subname}-component-metadata.jar
install -pm 644 plexus-component-annotations/target/*.jar \
 $RPM_BUILD_ROOT%{_javadir}/%{parent}/%{subname}-component-javadoc.jar

# pom
install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -pm 644 pom.xml $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{parent}-%{subname}.pom

install -pm 644 plexus-component-annotations/pom.xml \
         $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{parent}-%{subname}-component-annotations.pom
install -pm 644 plexus-container-default/pom.xml \
         $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{parent}-%{subname}-container-default.pom
install -pm 644 plexus-component-metadata/pom.xml \
         $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{parent}-%{subname}-component-metadata.pom
install -pm 644 plexus-component-javadoc/pom.xml \
         $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{parent}-%{subname}-component-javadoc.pom

%add_maven_depmap JPP.%{parent}-%{subname}.pom
%add_maven_depmap JPP.%{parent}-%{subname}-component-annotations.pom %{parent}/%{subname}-component-annotations.jar -f component-annotations
# component-api is now folded into container-default
%add_maven_depmap JPP.%{parent}-%{subname}-container-default.pom %{parent}/%{subname}-container-default.jar -a "org.codehaus.plexus:containers-component-api" -f container-default
%add_maven_depmap JPP.%{parent}-%{subname}-component-metadata.pom %{parent}/%{subname}-component-metadata.jar -f component-metadata
%add_maven_depmap JPP.%{parent}-%{subname}-component-javadoc.pom %{parent}/%{subname}-component-javadoc.jar -f component-javadoc

# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -pr target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}


%files -f .mfiles
%files component-annotations -f .mfiles-component-annotations
%files container-default -f .mfiles-container-default
%files component-metadata -f .mfiles-component-metadata
%files component-javadoc -f .mfiles-component-javadoc

%files javadoc
%doc %{_javadocdir}/*

%changelog
* Wed Nov 14 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.5.5-7
- Fix license tag (Plexus license was replaced by MIT some time ago)
- Update javadoc plugin BR version

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Feb 17 2012 Deepak Bhole <dbhole@redhat.com> - 1.5.5-5
- Resolves rhbz#791339
- Applied fix from Omair Majid <omajid at redhat dot com> to build with Java 7

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 28 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.5.5-3
- Fix maven3 build
- Use new add_maven_depmap macro

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
