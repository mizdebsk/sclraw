Name:           apache-parent
Version:        10
Release:        8%{?dist}
Summary:        Parent pom file for Apache projects
Group:          Development/Libraries
License:        ASL 2.0
URL:            http://apache.org/
Source0:        http://svn.apache.org/repos/asf/maven/pom/tags/apache-10/pom.xml
Source1:        http://www.apache.org/licenses/LICENSE-2.0.txt
BuildArch:      noarch

BuildRequires:  maven
BuildRequires:  jpackage-utils
BuildRequires:  apache-resource-bundles
BuildRequires:  maven-remote-resources-plugin

Requires:       jpackage-utils
Requires:       apache-resource-bundles
Requires:       maven-remote-resources-plugin

%description
This package contains the parent pom file for apache projects.


%prep
%setup -n %{name}-%{version} -Tc

# This simplifies work with child projects that can use generics
cp %{SOURCE0} .
sed -i 's:<source>1.4</source>:<source>1.5</source>:' pom.xml
sed -i 's:<target>1.4</target>:<target>1.5</target>:' pom.xml

cp %{SOURCE1} LICENSE

%build


%install
install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -pm 644 pom.xml \
        $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}.pom

%add_maven_depmap JPP-%{name}.pom

%check
mvn-rpmbuild verify

%files
%doc LICENSE
%{_mavenpomdir}/JPP-%{name}.pom
%{_mavendepmapfragdir}/%{name}

%changelog
* Tue Dec 18 2012 Michal Srb <msrb@redhat.com> - 10-8
- Added license (Resolves: #888287)

* Wed Nov 21 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 10-7
- Install patched pom not the original

* Fri Nov  2 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 10-6
- Add missing R: maven-remote-resources-plugin, apache-resource-bundles
- Add %%check to verify dependencies during build

* Thu Jul 26 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 10-5
- Make sure we generate 1.5 version bytecode

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Sep 13 2011 Andy Grimm <agrimm@gmail.com> 10-2
- Follow suggestions in BZ #736069

* Mon Aug 29 2011 Andy Grimm <agrimm@gmail.com> 10-1
- Initial Build
