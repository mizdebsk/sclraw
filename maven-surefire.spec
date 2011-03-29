Name:           maven-surefire
Version:        2.8
Release:        1%{?dist}
Epoch:          0
Summary:        Test framework project
License:        ASL 2.0
Group:          Development/Libraries
URL:            http://maven.apache.org/surefire/

Source0:        http://repo2.maven.org/maven2/org/apache/maven/surefire/surefire/%{version}/surefire-%{version}-source-release.zip
Source1:        %{name}-jpp-depmap.xml

# mockito is not available in Fedora yet
Patch0:         0001-Remove-mockito-dependency.patch

# remove test dep on htmlunit
Patch1:         0002-Remove-htmlunit-dependency.patch

BuildArch:      noarch
BuildRequires:  ant
BuildRequires:  ant-nodeps
BuildRequires:  classworlds
BuildRequires:  jpackage-utils >= 0:1.7.2
BuildRequires:  junit >= 3.8.2
BuildRequires:  plexus-utils
BuildRequires:  junit4
BuildRequires:  testng

BuildRequires:  maven
BuildRequires:  maven-compiler-plugin
BuildRequires:  maven-help-plugin
BuildRequires:  maven-install-plugin
BuildRequires:  maven-invoker-plugin
BuildRequires:  maven-jar-plugin
BuildRequires:  maven-javadoc-plugin
BuildRequires:  maven-plugin-plugin
BuildRequires:  maven-resources-plugin
BuildRequires:  maven-site-plugin
BuildRequires:  maven-shade-plugin
BuildRequires:  maven-shared-verifier
BuildRequires:  maven-surefire-maven-plugin

BuildRequires:  plexus-containers-component-api >= 1.0-0.a34
BuildRequires:  tomcat6
BuildRequires:  tomcat6-servlet-2.5-api
BuildRequires:  maven-plugin-testing-harness
BuildRequires:  bsf

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

%package plugin
Summary:                Surefire plugin for maven
Group:                  Development/Libraries
Requires:               maven-surefire = %{epoch}:%{version}-%{release}
Obsoletes:              maven2-plugin-surefire <= 0:2.0.4
Provides :              maven2-plugin-surefire = %{epoch}:%{version}-%{release}
Obsoletes:              maven-surefire-maven-plugin < 0:2.6
Provides :              maven-surefire-maven-plugin = %{epoch}:%{version}-%{release}

%description plugin
Maven surefire plugin for running tests via the surefire framework.

%package report-plugin
Summary:                Surefire reports plugin for maven
Group:                  Development/Libraries
Requires:               maven-surefire = %{epoch}:%{version}-%{release}
Obsoletes:              maven2-plugin-surefire-report <= 0:2.0.4
Provides :              maven2-plugin-surefire-report = %{epoch}:%{version}-%{release}
Obsoletes:              maven-surefire-report-maven-plugin < 0:2.6
Provides :              maven-surefire-report-maven-plugin = %{epoch}:%{version}-%{release}

%description report-plugin
Plugin for generating reports from surefire test runs.

%package provider-junit
Summary:                JUnit3 provider for Maven Surefire
Group:                  Development/Libraries
Requires:               junit
Requires:               maven-surefire = %{epoch}:%{version}-%{release}
Obsoletes:              maven2-plugin-surefire-report <= 0:2.0.4O
#Obsoletes:              maven-surefire-junit = 2.3.1
Provides:              maven2-plugin-surefire-report = %{epoch}:%{version}-%{release}
#Provides:              maven-surefire-junit = 2.3.1

%description provider-junit
JUnit3 provider for Maven Surefire.

%package provider-junit4
Summary:                JUnit4 provider for Maven Surefire
Group:                  Development/Libraries
Requires:               maven-surefire = %{epoch}:%{version}-%{release}
Requires:               junit4

%description provider-junit4
JUnit4 provider for Maven Surefire.

%package provider-testng
Summary:                TestNG provider for Maven Surefire
Group:                  Development/Libraries
Requires:               maven-surefire = %{epoch}:%{version}-%{release}
Requires:               testng

%description provider-testng
TestNG provider for Maven Surefire.

%package -n maven-failsafe-plugin
Summary:                Maven plugin for running integration tests
Group:                  Development/Libraries
Requires:               maven-surefire = %{epoch}:%{version}-%{release}

%description -n maven-failsafe-plugin
The Failsafe Plugin is designed to run integration tests while the
Surefire Plugins is designed to run unit. The name (failsafe) was
chosen both because it is a synonym of surefire and because it implies
that when it fails, it does so in a safe way.

If you use the Surefire Plugin for running tests, then when you have a
test failure, the build will stop at the integration-test phase and
your integration test environment will not have been torn down
correctly.

The Failsafe Plugin is used during the integration-test and verify
phases of the build lifecycle to execute the integration tests of an
application. The Failsafe Plugin will not fail the build during the
integration-test phase thus enabling the post-integration-test phase
to execute.

%package javadoc
Summary:          Javadoc for %{name}
Group:            Documentation

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -n surefire-%{version}

sed -i 's:<version>2.7.2</version>:<version>${project.version}</version>:' \
       surefire-integration-tests/pom.xml

%patch0 -p1 -b .sav
%patch1 -p1 -b .sav

%build
# tests turned off because they need jmock
mvn-rpmbuild -e \
        -Dmaven.local.depmap.file=%{SOURCE1} \
        -Dmaven.test.skip=true \
        install javadoc:aggregate

%install
# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}/maven-surefire
install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}

install -pm 644 maven-surefire-plugin/target/maven-surefire-plugin-*.jar $RPM_BUILD_ROOT%{_javadir}/maven-surefire/maven-plugin.jar
%add_to_maven_depmap org.apache.maven.surefire maven-surefire-plugin %{version} JPP/maven-surefire maven-plugin
install -pm 644 maven-surefire-plugin/pom.xml $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.maven-surefire-maven-plugin.pom
install -pm 644 maven-surefire-plugin/pom.xml $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.maven2.plugins-surefire-plugin.pom

install -pm 644 maven-surefire-common/target/maven-surefire-common-*.jar $RPM_BUILD_ROOT%{_javadir}/maven-surefire/common.jar
%add_to_maven_depmap org.apache.maven.surefire maven-surefire-common %{version} JPP/maven-surefire common
install -pm 644 maven-surefire-common/pom.xml $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.maven-surefire-common.pom

install -pm 644 maven-surefire-report-plugin/target/maven-surefire-report-plugin-*.jar $RPM_BUILD_ROOT%{_javadir}/maven-surefire/report-maven-plugin.jar
%add_to_maven_depmap org.apache.maven.surefire maven-surefire-report-plugin %{version} JPP/maven-surefire report-maven-plugin
install -pm 644 maven-surefire-report-plugin/pom.xml $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.maven-surefire-report-maven-plugin.pom

install -pm 644 surefire-api/target/original-surefire-api-*.jar $RPM_BUILD_ROOT%{_javadir}/maven-surefire/api.jar
%add_to_maven_depmap org.apache.maven.surefire surefire-api %{version} JPP/maven-surefire api
install -pm 644 surefire-api/pom.xml $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.maven-surefire-api.pom

install -pm 644 surefire-booter/target/surefire-booter-*.jar $RPM_BUILD_ROOT%{_javadir}/maven-surefire/booter.jar
%add_to_maven_depmap org.apache.maven.surefire surefire-booter %{version} JPP/maven-surefire booter
install -pm 644 surefire-booter/pom.xml $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.maven-surefire-booter.pom

install -pm 644 surefire-providers/common-junit3/target/common-junit3-*.jar $RPM_BUILD_ROOT%{_javadir}/maven-surefire/common-junit.jar
%add_to_maven_depmap org.apache.maven.surefire common-junit3 %{version} JPP/maven-surefire common-junit
install -pm 644 surefire-providers/common-junit3/pom.xml $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.maven-surefire-common-junit.pom

install -pm 644 surefire-providers/surefire-junit3/target/original-surefire-junit3-*.jar $RPM_BUILD_ROOT%{_javadir}/maven-surefire/junit.jar
%add_to_maven_depmap org.apache.maven.surefire surefire-junit3 %{version} JPP/maven-surefire junit
%add_to_maven_depmap org.apache.maven.surefire surefire-junit %{version} JPP/maven-surefire junit
install -pm 644 surefire-providers/surefire-junit3/pom.xml $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.maven-surefire-junit.pom

install -pm 644 surefire-providers/common-junit4/target/common-junit4-*.jar $RPM_BUILD_ROOT%{_javadir}/maven-surefire/common-junit4.jar
%add_to_maven_depmap org.apache.maven.surefire common-junit4 %{version} JPP/maven-surefire common-junit4
install -pm 644 surefire-providers/common-junit4/pom.xml $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.maven-surefire-common-junit4.pom

install -pm 644 surefire-providers/surefire-junit4/target/original-surefire-junit4-*.jar $RPM_BUILD_ROOT%{_javadir}/maven-surefire/junit4.jar
%add_to_maven_depmap org.apache.maven.surefire surefire-junit4 %{version} JPP/maven-surefire junit4
install -pm 644 surefire-providers/surefire-junit4/pom.xml $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.maven-surefire-junit4.pom

install -pm 644 surefire-providers/surefire-junit47/target/original-surefire-junit47-*.jar $RPM_BUILD_ROOT%{_javadir}/maven-surefire/junit47.jar
%add_to_maven_depmap org.apache.maven.surefire surefire-junit47 %{version} JPP/maven-surefire junit47
install -pm 644 surefire-providers/surefire-junit47/pom.xml $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.maven-surefire-junit47.pom

install -pm 644 surefire-providers/surefire-testng/target/surefire-testng-*.jar $RPM_BUILD_ROOT%{_javadir}/maven-surefire/testng.jar
%add_to_maven_depmap org.apache.maven.surefire surefire-testng %{version} JPP/maven-surefire testng
install -pm 644 surefire-providers/surefire-testng/pom.xml $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.maven-surefire-testng.pom

%add_to_maven_depmap org.apache.maven.surefire providers %{version} JPP/maven-surefire providers
install -pm 644 surefire-providers/pom.xml $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.maven-surefire-providers.pom

install -pm 644 maven-failsafe-plugin/target/maven-failsafe-plugin*.jar $RPM_BUILD_ROOT%{_javadir}/maven-failsafe-plugin.jar
%add_to_maven_depmap org.apache.maven.plugins maven-failsafe-plugin %{version} JPP maven-failsafe-plugin
install -pm 644 maven-failsafe-plugin/pom.xml $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-maven-failsafe-plugin.pom

install -pm 644 pom.xml $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.maven-surefire-main.pom
%add_to_maven_depmap org.apache.maven.surefire surefire %{version} JPP/maven-surefire main

# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -pr target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}

# Create compatibility links
ln -s %{_javadir}/maven-surefire/api.jar \
      $RPM_BUILD_ROOT%{_javadir}/maven-surefire/surefire.jar

install -dm 755 $RPM_BUILD_ROOT%{_datadir}/maven2/plugins
ln -s %{_javadir}/maven-surefire/maven-plugin.jar \
      $RPM_BUILD_ROOT%{_datadir}/maven2/plugins/surefire-plugin.jar

ln -s %{_javadir}/maven-surefire/report-maven-plugin.jar \
      $RPM_BUILD_ROOT%{_datadir}/maven2/plugins/surefire-report-plugin.jar

%pre javadoc
# workaround for rpm bug, can be removed in F-18
[ $1 -gt 1 ] && [ -L %{_javadocdir}/%{name} ] && \
rm -rf $(readlink -f %{_javadocdir}/%{name}) %{_javadocdir}/%{name} || :


%post
%update_maven_depmap

%postun
%update_maven_depmap

%files
%defattr(-,root,root,-)
%dir %{_javadir}/maven-surefire
%{_javadir}/maven-surefire/api.jar
%{_javadir}/maven-surefire/booter.jar
%{_javadir}/maven-surefire/surefire.jar
%{_javadir}/maven-surefire/common.jar
%{_mavenpomdir}/*
%{_mavendepmapfragdir}/*

%files plugin
%defattr(-,root,root,-)
%{_javadir}/maven-surefire/maven-plugin.jar
%dir %{_datadir}/maven2/plugins
%{_datadir}/maven2/plugins/surefire-plugin.jar

%files report-plugin
%defattr(-,root,root,-)
%{_javadir}/maven-surefire/report-maven-plugin.jar
%dir %{_datadir}/maven2/plugins
%{_datadir}/maven2/plugins/surefire-report-plugin.jar

%files provider-junit
%defattr(-,root,root,-)
%{_javadir}/maven-surefire/junit.jar
%{_javadir}/maven-surefire/common-junit.jar

%files provider-junit4
%defattr(-,root,root,-)
%{_javadir}/maven-surefire/junit4.jar
%{_javadir}/maven-surefire/junit47.jar
%{_javadir}/maven-surefire/common-junit4.jar

%files provider-testng
%defattr(-,root,root,-)
%{_javadir}/maven-surefire/testng.jar

%files -n maven-failsafe-plugin
%defattr(-,root,root,-)
%{_javadir}/maven-failsafe-plugin.jar

%files javadoc
%defattr(-,root,root,-)
%doc %{_javadocdir}/*

%changelog
* Tue Mar 29 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:2.8-1
- Update to latest upstream version (2.8)

* Mon Mar  7 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:2.7.2-1
- Update to latest version (2.7.2)
- Add common-junit* jars to distribution
- Versionless javadocs
- Use maven 3 to build

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 3 2011 Alexander Kurtakov <akurtako@redhat.com> 0:2.7.1-2
- Fix junit3 depmap.

* Wed Dec 29 2010 Alexander Kurtakov <akurtako@redhat.com> 0:2.7.1-1
- Update to 2.7.1.

* Wed Dec  8 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:2.6-3
- Add proper Requires on junit/junit4/testng to providers

* Fri Oct 29 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:2.6-2
- Add main pom.xml

* Mon Aug 30 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:2.6-1
- Rename subpackages to not repeat "maven" twice
- Update to latest upstream version
- Add common jar to files
- Introduce maven-failsafe-plugin sub-package
- Cleanups

* Mon Aug 31 2009 Andrew Overholt <overholt@redhat.com> 0:2.3-7.7
- Bump release to rebuild

* Mon Aug 31 2009 Alexander Kurtakov <akurtako@redhat.com> 0:2.3-7.6
- Really remove maven2-plugin-surefire BR.

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
