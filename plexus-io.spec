Name:           plexus-io
Version:        1.0.1
Release:        1%{?dist}
Summary:        Plexus IO Components

Group:          Development/Libraries
License:        ASL 2.0
URL:            http://plexus.codehaus.org/plexus-components/plexus-io
#svn export http://svn.codehaus.org/plexus/plexus-components/tags/plexus-io-1.0.1/
#tar caf plexus-io-1.0.1.tar.xz plexus-io-1.0.1/      
Source0:        plexus-io-%{version}.tar.xz
BuildArch: noarch

BuildRequires: java-devel >= 1:1.6.0 
BuildRequires:  jpackage-utils

BuildRequires: plexus-utils
BuildRequires: plexus-container-default
BuildRequires: maven
BuildRequires: maven-resources-plugin
BuildRequires: maven-compiler-plugin
BuildRequires: maven-jar-plugin
BuildRequires: maven-install-plugin
BuildRequires: maven-javadoc-plugin
BuildRequires: maven-surefire-plugin
BuildRequires: maven-surefire-provider-junit
BuildRequires: maven-doxia-sitetools
BuildRequires: plexus-maven-plugin
Requires:  jpackage-utils
Requires: plexus-utils
Requires: plexus-container-default

Requires(post): jpackage-utils
Requires(postun): jpackage-utils

%description
Plexus IO is a set of plexus components, which are designed for use
in I/O operations. 

%package javadoc
Group:          Documentation
Summary:        Javadoc for %{name}
Requires:       jpackage-utils

%description javadoc
API documentation for %{name}.


%prep
%setup -q 

%build
mvn-rpmbuild install javadoc:javadoc

%install
# jars
install -d -m 0755 %{buildroot}%{_javadir}/plexus
install -m 644 target/%{name}-%{version}.jar   %{buildroot}%{_javadir}/plexus/io.jar

%add_to_maven_depmap org.codehaus.plexus %{name} %{version} JPP/plexus io

# poms
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -pm 644 pom.xml \
    %{buildroot}%{_mavenpomdir}/JPP.%{name}.pom

# javadoc
install -d -m 0755 %{buildroot}%{_javadocdir}/%{name}
cp -pr target/site/api*/* %{buildroot}%{_javadocdir}/%{name}/

%post
%update_maven_depmap

%postun
%update_maven_depmap

%files
%defattr(-,root,root,-)
%doc NOTICE.txt
%{_javadir}/plexus/*.jar
%{_mavenpomdir}/*
%{_mavendepmapfragdir}/*

%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/%{name}

%changelog
* Tue May 17 2011 Alexander Kurtakov <akurtako@redhat.com> 1.0.1-1
- Update to upstream 1.0.1.
- Adapt to current guidelines.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.3.a5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 23 2009 Alexander Kurtakov <akurtako@redhat.com> 1.0-0.2.a5
- Fix review comments.

* Wed Dec 23 2009 Alexander Kurtakov <akurtako@redhat.com> 1.0-0.1.a5.1
- Initial package
