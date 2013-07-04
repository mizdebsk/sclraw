%global namedreltag .NOTHING
%global namedversion %{version}%{?namedreltag}

Name:             cdi-api
Version:          1.1
Release:          1%{?dist}
Summary:          CDI API
Group:            Development/Libraries
License:          ASL 2.0
URL:              http://seamframework.org/Weld
Source0:          https://github.com/cdi-spec/cdi/archive/%{version}.tar.gz

BuildArch:        noarch

BuildRequires:    maven-local
BuildRequires:    maven-compiler-plugin
BuildRequires:    maven-install-plugin
BuildRequires:    maven-jar-plugin
BuildRequires:    maven-javadoc-plugin
BuildRequires:    maven-surefire-provider-testng
BuildRequires:    maven-enforcer-plugin
BuildRequires:    testng
BuildRequires:    jboss-el-2.2-api
BuildRequires:    jboss-interceptors-1.1-api
BuildRequires:    jboss-ejb-3.1-api
BuildRequires:    geronimo-annotation
BuildRequires:    geronimo-parent-poms
BuildRequires:    weld-parent
BuildRequires:    maven-plugin-build-helper

%description
APIs for JSR-299: Contexts and Dependency Injection for Java EE

%package javadoc
Summary:          Javadocs for %{name}

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -n cdi-%{version}

%build
cd api
%mvn_build

%install
cd api
%mvn_install

%files -f api/.mfiles
%dir %{_javadir}/%{name}

%files javadoc -f api/.mfiles-javadoc

%changelog
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

* Wed Mar 16 2012 Asaf Shakarchi <asaf@redhat.com> 1.0-2.SP4
- Added required dependencies, modified patches and cleaned spec.

* Mon Feb 20 2012 Marek Goldmann <mgoldman@redhat.com> 1.0-1.SP4
- Initial packaging

