%global short_name maven-plugins

Name:           %{short_name}-pom
Version:        23
Release:        7%{?dist}
Summary:        Maven Plugins POM
BuildArch:      noarch
Group:          Development/Libraries
License:        ASL 2.0
URL:            http://maven.apache.org/plugins/
Source:         http://repo.maven.apache.org/maven2/org/apache/maven/plugins/%{short_name}/%{version}/%{short_name}-%{version}-source-release.zip

BuildRequires:  maven-local

%description
This package provides Maven Plugins parent POM used by different
Apache Maven plugins.

%prep
%setup -q -n %{short_name}-%{version}
# Enforcer plugin is used to ban plexus-component-api.
%pom_remove_plugin :maven-enforcer-plugin

%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%doc LICENSE NOTICE

%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 23-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 23-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 23-5
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Fri Jan  4 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 23-4
- Disable maven-enforcer-plugin
- Build with xmvn

* Thu Nov 15 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 23-3
- Add missing R: maven-enforcer-plugin

* Fri Nov  2 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 23-2
- Install license files

* Wed Oct 31 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 23-1
- Initial packaging
