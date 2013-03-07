Name:           maven-compiler-plugin
Version:        3.0
Release:        2%{?dist}
Summary:        Maven Compiler Plugin

Group:          Development/Libraries
License:        ASL 2.0
URL:            http://maven.apache.org/plugins/maven-compiler-plugin
Source0:        http://repo1.maven.org/maven2/org/apache/maven/plugins/%{name}/%{version}/%{name}-%{version}-source-release.zip

BuildArch: noarch

BuildRequires:  java-devel >= 1:1.6.0
BuildRequires:  maven-local
BuildRequires:  maven-plugin-plugin
BuildRequires:  maven-shared-incremental
BuildRequires:  maven-surefire-provider-junit
BuildRequires:  maven-doxia-sitetools
BuildRequires:  maven-plugin-testing-harness
BuildRequires:  maven-toolchain
BuildRequires:  plexus-compiler >= 2.0

Provides:       maven2-plugin-compiler = %{version}-%{release}
Obsoletes:      maven2-plugin-compiler <= 0:2.0.8

%description
The Compiler Plugin is used to compile the sources of your project.

%package javadoc
Group:          Documentation
Summary:        Javadoc for %{name}

%description javadoc
API documentation for %{name}.

%prep
%setup -q 

%build
%mvn_build -f

%install
%mvn_install

%files -f .mfiles
%doc LICENSE NOTICE

%files javadoc -f .mfiles-javadoc
%doc LICENSE NOTICE

%changelog
* Tue Mar 05 2013 Michal Srb <msrb@redhat.com> - 3.0-2
- Build against proper plexus-compiler

* Tue Jan 15 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0-1
- Update to upstream version 3.0
- Build with xmvn
- Install license files, resolves: rhbz#895544

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 19 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.5.1-1
- Updated to latest upstream version (2.5.1)

* Wed May 23 2012 Tomas Radej <tradej@redhat.com> - 2.4-1
- Updated to latest upstream version
- Guidelines fixes + Removed RPM workaround

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 27 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.3.2-4
- Add few missing (Build)requires
- Remove post(un) scriptlets with update_maven_depmap
- Use new add_maven_depmap macro

* Fri Jun 3 2011 Alexander Kurtakov <akurtako@redhat.com> 2.3.2-3
- Do not require maven2.
- Guidelines fixes.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 19 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.3.2-1
- Update to latest version (2.3.2)
- Modifications according to new guidelines
- Build with maven 3

* Wed May 12 2010 Alexander Kurtakov <akurtako@redhat.com> 2.0.2-2
- Add missing requires.

* Tue May 11 2010 Alexander Kurtakov <akurtako@redhat.com> 2.0.2-1
- Initial package.
