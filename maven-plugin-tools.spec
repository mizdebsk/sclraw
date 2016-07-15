Name:           maven-plugin-tools
Version:        3.4
Release:        7%{?dist}
Epoch:          0
Summary:        Maven Plugin Tools
License:        ASL 2.0
URL:            http://maven.apache.org/plugin-tools/
BuildArch:      noarch

Source0:        http://repo2.maven.org/maven2/org/apache/maven/plugin-tools/%{name}/%{version}/%{name}-%{version}-source-release.zip

Patch0001:      0001-Remove-dep-on-qdox.patch
Patch0002:      0002-Remove-plexus-velocity.patch
Patch0003:      0003-Remove-doxia.patch
Patch0004:      0004-Remove-dep-on-jtidy.patch
Patch0005:      0005-Avoid-duplicate-MOJO-parameters.patch

BuildRequires:  maven-local
BuildRequires:  mvn(org.apache.maven:maven-artifact)
BuildRequires:  mvn(org.apache.maven:maven-compat)
BuildRequires:  mvn(org.apache.maven:maven-core)
BuildRequires:  mvn(org.apache.maven:maven-model)
BuildRequires:  mvn(org.apache.maven:maven-parent:pom:)
BuildRequires:  mvn(org.apache.maven:maven-plugin-api)
BuildRequires:  mvn(org.codehaus.modello:modello-maven-plugin)
BuildRequires:  mvn(org.codehaus.plexus:plexus-component-annotations)
BuildRequires:  mvn(org.codehaus.plexus:plexus-component-metadata)
BuildRequires:  mvn(org.codehaus.plexus:plexus-utils)
BuildRequires:  mvn(org.ow2.asm:asm)
BuildRequires:  mvn(org.ow2.asm:asm-commons)

BuildRequires:  maven-plugin-plugin

%description
The Maven Plugin Tools contains the necessary tools to be able to produce Maven
Plugins in a variety of languages.

%package -n maven-plugin-annotations
Summary:        Maven Plugin Java 5 Annotations
Obsoletes:      maven-plugin-annotations < 0:%{version}-%{release}

%description -n maven-plugin-annotations
This package contains Java 5 annotations to use in Mojos.

%package -n maven-plugin-plugin
Summary:        Maven Plugin Plugin

%description -n maven-plugin-plugin
The Plugin Plugin is used to create a Maven plugin descriptor for any Mojo's
found in the source tree, to include in the JAR. It is also used to generate
Xdoc files for the Mojos as well as for updating the plugin registry, the
artifact metadata and a generic help goal.

%package annotations
Summary:        Maven Plugin Tool for Annotations

%description annotations
This package provides Java 5 annotation tools for use with Apache Maven.

%package api
Summary:        Maven Plugin Tools APIs
Obsoletes:      maven-shared-plugin-tools-api < 0:%{version}-%{release}
Provides:       maven-shared-plugin-tools-api = 0:%{version}-%{release}

%description api
The Maven Plugin Tools API provides an API to extract information from
and generate documentation for Maven Plugins.

%package generators
Summary:        Maven Plugin Tools Generators

%description generators
The Maven Plugin Tools Generators provides content generation
(documentation, help) from plugin descriptor.

# This "javadocs" package violates packaging guidelines as of Sep 6 2012. The
# subpackage name "javadocs" instead of "javadoc" is intentional. There was a
# consensus that current naming scheme should be kept, even if it doesn't
# conform to the guidelines.  mizdebsk, September 2012
%package javadocs
Summary:        Javadoc for %{name}

%description javadocs
API documentation for %{name}.


%prep
%setup -q
%patch0001 -p1
%patch0002 -p1
%patch0003 -p1
%patch0004 -p1
%patch0005 -p1

%pom_remove_plugin :maven-plugin-plugin maven-plugin-plugin
%pom_remove_plugin :maven-enforcer-plugin maven-plugin-plugin
%pom_remove_plugin :maven-source-plugin maven-plugin-tools-annotations

# Modules we don't need
rm -rf maven-script maven-plugin-tools-java maven-plugin-tools-javadoc
%pom_disable_module maven-script
%pom_disable_module maven-plugin-tools-java
%pom_disable_module maven-plugin-tools-javadoc

%pom_remove_dep :maven-plugin-tools-java maven-plugin-plugin

# These require doxia
rm -f maven-plugin-tools-generators/src/main/java/org/apache/maven/tools/plugin/generator/PluginXdocGenerator.java
rm -f maven-plugin-plugin/src/main/java/org/apache/maven/plugin/plugin/PluginReport.java
# These require velocity
rm -f maven-plugin-plugin/src/main/java/org/apache/maven/plugin/plugin/HelpGeneratorMojo.java
rm -f maven-plugin-tools-generators/src/main/java/org/apache/maven/tools/plugin/generator/PluginHelpGenerator.java
# These require maven2
rm -f maven-plugin-plugin/src/main/java/org/apache/maven/plugin/plugin/UpdatePluginRegistryMojo.java

%pom_remove_dep :qdox maven-plugin-tools-annotations
%pom_remove_dep :plexus-archiver maven-plugin-tools-annotations

%pom_remove_dep :velocity maven-plugin-plugin
%pom_remove_dep :plexus-velocity maven-plugin-plugin
%pom_remove_dep :velocity maven-plugin-tools-generators
%pom_remove_dep :plexus-velocity maven-plugin-tools-generators

%pom_remove_dep :doxia-sink-api maven-plugin-plugin
%pom_remove_dep :doxia-site-renderer maven-plugin-plugin
%pom_remove_dep :maven-reporting-api maven-plugin-plugin
%pom_remove_dep :maven-reporting-impl maven-plugin-plugin
%pom_remove_dep :maven-reporting-api maven-plugin-tools-generators

%pom_remove_dep :jtidy maven-plugin-tools-generators

# Maven 2
%pom_xpath_set pom:mavenVersion 3.3.9
%pom_change_dep -r :maven-project :maven-core
%pom_change_dep -r :maven-repository-metadata :maven-compat
%pom_remove_dep -r :maven-plugin-descriptor
%pom_remove_dep -r :maven-plugin-registry
%pom_remove_dep -r :maven-artifact-manager



%pom_xpath_inject "pom:project/pom:properties" "
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    <project.reporting.outputEncoding>UTF-8</project.reporting.outputEncoding>"

%build
%mvn_build -s -f

%install
%mvn_install


%files -f .mfiles-maven-plugin-tools
%doc LICENSE NOTICE

%files -n maven-plugin-annotations -f .mfiles-maven-plugin-annotations

%files -n maven-plugin-plugin -f .mfiles-maven-plugin-plugin

%files annotations -f .mfiles-maven-plugin-tools-annotations

%files api -f .mfiles-maven-plugin-tools-api

%files generators -f .mfiles-maven-plugin-tools-generators

%files javadocs -f .mfiles-javadoc
%doc LICENSE NOTICE


%changelog
* Fri Jul 15 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:3.4-7
- Remove uneeded plugins

* Fri Jul 15 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:3.4-6
- HACK HACK HACK Disable unneeded features

* Thu May 12 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:3.4-5
- Port to plexus-utils 3.0.24

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0:3.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:3.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Mar 16 2015 Michael Simacek <msimacek@redhat.com> - 0:3.4-2
- Prevent NPE when setting description element

* Mon Mar 16 2015 Michael Simacek <msimacek@redhat.com> - 0:3.4-1
- Update to upstream version 3.4

* Tue Oct 28 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:3.3-4
- Port to QDox 2.0

* Tue Oct 14 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:3.3-3
- Remove legacy Obsoletes/Provides for maven2 plugin

* Mon Oct 13 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:3.3-2
- Port to maven-reporting-impl 2.3

* Thu Jun 19 2014 Michal Srb <msrb@redhat.com> - 0:3.3-1
- Update to upstream version 3.3

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:3.1-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:3.1-19
- Use Requires: java-headless rebuild (#1067528)

* Mon Jan 27 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:3.1-18
- Use Maven 3.x APIs

* Fri Jan 10 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:3.1-17
- Remove explicit requires
- Resolves: rhbz#1051527

* Fri Sep 20 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:3.1-16
- Disable test dependencies

* Fri Sep 20 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:3.1-15
- Fix com.sun:tools dependency

* Thu Aug 29 2013 Michal Srb <msrb@redhat.com> - 0:3.1-14
- Adapt to current guidelines (Resolves: #960526)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:3.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May  7 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:3.1-12
- Disable resolution of test artifacts

* Thu Apr 18 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:3.1-11
- Remove test dependencies

* Mon Mar 11 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:3.1-10
- Add patch for MPLUGIN-242
- Resolves: rhbz#920042

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:3.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 0:3.1-8
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Fri Dec 21 2012 Michal Srb <msrb@redhat.com> - 0:3.1-7
- Migrated from maven-doxia to doxia subpackage (Resolves: #889147)

* Wed Nov 14 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:3.1-6
- Skip running tests because they are failing

* Tue Sep 11 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:3.1-5
- Add missing requires

* Tue Sep 11 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:3.1-4
- Rebuild without bootstrap

* Tue Sep 11 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:3.1-3
- Add obsoletes for maven-plugin-annotations

* Mon Sep 10 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:3.1-2
- Bump release

* Fri Sep  7 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:3.1-1
- Update to upstream version 3.1
- Bootstrap using prebuilt upstream binaries

* Thu Sep  6 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.7-7
- Remove rpm bug workaround

* Tue Aug 28 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.7-6
- Wrap descriptions at column 80
- Install LICENSE and NOTICE files

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov 16 2011 Jaromir Capik <jcapik@redhat.com> -  0:2.7-3
- Missing com.sun.javadoc / com.sun.tools.doclet forced in the POM

* Tue Aug 16 2011 Jaromir Capik <jcapik@redhat.com> -  0:2.7-2
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
