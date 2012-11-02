%global short_name maven-plugins

Name:           %{short_name}-pom
Version:        23
Release:        2%{?dist}
Summary:        Maven Plugins POM
BuildArch:      noarch
Group:          Development/Libraries
License:        ASL 2.0
URL:            http://maven.apache.org/plugins/
Source:         http://repo.maven.apache.org/maven2/org/apache/maven/plugins/%{short_name}/%{version}/%{short_name}-%{version}-source-release.zip

BuildRequires:  jpackage-utils
BuildRequires:  maven
BuildRequires:  maven-enforcer-plugin

Requires:       jpackage-utils

%description
This package provides Maven Plugins parent POM used by different
Apache Maven plugins.

%prep
%setup -q -n %{short_name}-%{version}

%check
mvn-rpmbuild verify

%install
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -p -m 644 pom.xml %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom
%add_maven_depmap JPP-%{name}.pom

%files
%doc LICENSE NOTICE
%{_mavenpomdir}/JPP-%{name}.pom
%{_mavendepmapfragdir}/%{name}

%changelog
* Fri Nov  2 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 23-2
- Install license files

* Wed Oct 31 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 23-1
- Initial packaging
