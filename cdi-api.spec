%global namedreltag .NOTHING
%global namedversion %{version}%{?namedreltag}

Name:             cdi-api
Version:          1.1
Release:          10%{?dist}
Summary:          CDI API
License:          ASL 2.0
URL:              http://seamframework.org/Weld
Source0:          https://github.com/cdi-spec/cdi/archive/%{version}.tar.gz

BuildArch:        noarch
BuildRequires:    maven-local
# geronimo-annotation
BuildRequires:    mvn(javax.annotation:jsr250-api)
BuildRequires:    mvn(javax.el:javax.el-api)
BuildRequires:    mvn(javax.inject:javax.inject)
BuildRequires:    mvn(org.apache.geronimo.specs:specs:pom:)
BuildRequires:    mvn(org.apache.maven.plugins:maven-enforcer-plugin)
BuildRequires:    mvn(org.apache.maven.surefire:surefire-testng)
BuildRequires:    mvn(org.codehaus.mojo:build-helper-maven-plugin)
BuildRequires:    mvn(org.jboss.spec.javax.interceptor:jboss-interceptors-api_1.2_spec)
BuildRequires:    mvn(org.jboss.spec.javax.ejb:jboss-ejb-api_3.1_spec)
BuildRequires:    mvn(org.jboss.weld:weld-parent:pom:)
BuildRequires:    mvn(org.testng:testng::jdk15:)

Provides:         javax.enterprise.inject

%description
APIs for JSR-299: Contexts and Dependency Injection for Java EE

%package javadoc
Summary:          Javadoc for %{name}

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -n cdi-%{version}

# Generate OSGI info
%pom_xpath_set pom:project/pom:packaging bundle api
%pom_xpath_inject "pom:project" "
    <build>
      <plugins>
        <plugin>
          <groupId>org.apache.felix</groupId>
          <artifactId>maven-bundle-plugin</artifactId>
          <extensions>true</extensions>
          <configuration>
            <instructions>
              <_nouses>true</_nouses>
              <Export-Package>javax.decorator.*;javax.enterprise.context.*;javax.enterprise.event.*;javax.enterprise.inject.*;javax.enterprise.util.*</Export-Package>
            </instructions>
          </configuration>
        </plugin>
      </plugins>
    </build>" api

%pom_xpath_set "pom:dependency[pom:groupId = 'javax.el']/pom:artifactId" javax.el-api api

cd api
# J2EE API directory
%mvn_file :{cdi-api} %{name}/@1 javax.enterprise.inject/@1

# Use newer version of interceptors API
%pom_remove_dep "org.jboss.spec.javax.interceptor:jboss-interceptors-api_1.1_spec"
%pom_add_dep "org.jboss.spec.javax.interceptor:jboss-interceptors-api_1.2_spec"

%build
cd api
%mvn_build

%install
cd api
%mvn_install

build-jar-repository %{buildroot}%{_javadir}/javax.enterprise.inject/ \
                     jboss-interceptors-1.2-api geronimo-annotation javax.inject

%files -f api/.mfiles
%dir %{_javadir}/%{name}
%{_javadir}/javax.enterprise.inject/

%files javadoc -f api/.mfiles-javadoc

%changelog
* Wed May 20 2015 gil cattaneo <puntogil@libero.it> 1.1-10
- rebuilt for upgrade el apis gid:aid (rhbz#1223468)
- adapt to current guideline
- use mvn()-like BRs
- fix rpmlint problem in changelog entries

* Tue Mar 24 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.1-9
- Fix interceptors symlink

* Mon Mar 23 2015 Marek Goldmann <mgoldman@redhat.com> - 1.1-8
- Switch to interceptors 1.2

* Mon Nov 17 2014 Alexander Kurtakov <akurtako@redhat.com> 1.1-7
- Rebuild to fix broken symlink to jboss-interceptors.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 1.1-5
- Use Requires: java-headless rebuild (#1067528)

* Tue Aug 13 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.1-4
- Add javax.enterprise.inject provides and directory

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 23 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.1-2
- Generate OSGi metadata
- Resolves: rhbz#987111

* Thu Jul 04 2013 Marek Goldmann <mgoldman@redhat.com> - 1.1-1
- Upstream release 1.1
- New guidelines

* Sat Mar 02 2013 Mat Booth <fedora@matbooth.co.uk> - 1.0-9.SP4
- Add missing BR, fixes FTBFS rhbz #913916

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-8.SP4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.0-7.SP4
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Tue Dec 04 2012 Marek Goldmann <mgoldman@redhat.com> - 1.0-6.SP4
- Added missing BR

* Tue Dec 04 2012 Marek Goldmann <mgoldman@redhat.com> - 1.0-5.SP4
- Added missing BR/R
- Simplified the spec file
- Removed unnecessary patch

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-4.SP4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Mar 25 2012 Asaf Shakarchi <asaf@redhat.com> 1.0-3.SP4
- Fixed changelog versions.

* Fri Mar 16 2012 Asaf Shakarchi <asaf@redhat.com> 1.0-2.SP4
- Added required dependencies, modified patches and cleaned spec.

* Mon Feb 20 2012 Marek Goldmann <mgoldman@redhat.com> 1.0-1.SP4
- Initial packaging
