Name:           maven-compiler-plugin
Version:        2.3.2
Release:        1%{?dist}
Summary:        Maven Compiler Plugin

Group:          Development/Libraries
License:        ASL 2.0
URL:            http://maven.apache.org/plugins/maven-compiler-plugin
#svn export http://svn.apache.org/repos/asf/maven/plugins/tags/maven-compiler-plugin-2.3.2 maven-compiler-plugin-2.3.2
#tar caf maven-compiler-plugin-2.3.2.tar.xz maven-compiler-plugin-2.3.2/
Source0:        %{name}-%{version}.tar.xz

BuildArch: noarch

BuildRequires: java-devel >= 1:1.6.0
BuildRequires: maven2
BuildRequires: maven-plugin-plugin
BuildRequires: maven-compiler-plugin
BuildRequires: maven-jar-plugin
BuildRequires: maven-install-plugin
BuildRequires: maven-resources-plugin
BuildRequires: maven-javadoc-plugin
BuildRequires: maven-surefire-maven-plugin
BuildRequires: maven-surefire-provider-junit
BuildRequires: maven-doxia-sitetools
BuildRequires: maven-shared-plugin-testing-harness

Requires:      maven2
Requires:      jpackage-utils
Requires:      java
Requires(post):       jpackage-utils
Requires(postun):     jpackage-utils

Provides:       maven2-plugin-compiler = %{version}-%{release}
Obsoletes:      maven2-plugin-compiler <= 0:2.0.8

%description
The Compiler Plugin is used to compile the sources of your project.

%package javadoc
Group:          Documentation
Summary:        Javadoc for %{name}
Requires:       jpackage-utils

%description javadoc
API documentation for %{name}.


%prep
%setup -q #You may need to update this according to your Source0

%build
mvn-local -e \
        -Dmaven.test.skip=true \
        install javadoc:javadoc

%install

# jars
install -d -m 0755 %{buildroot}%{_javadir}
install -m 644 target/%{name}-%{version}.jar   %{buildroot}%{_javadir}/%{name}.jar

%add_to_maven_depmap org.apache.maven.plugins maven-compiler-plugin %{version} JPP maven-compiler-plugin

# poms
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -pm 644 pom.xml \
    %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom

# javadoc
install -d -m 0755 %{buildroot}%{_javadocdir}/%{name}
cp -pr target/site/api*/* %{buildroot}%{_javadocdir}/%{name}

%pre javadoc
# workaround for rpm bug, can be removed in F-17
[ $1 -gt 1 ] && [ -L %{_javadocdir}/%{name} ] && \
rm -rf $(readlink -f %{_javadocdir}/%{name}) %{_javadocdir}/%{name} || :

%post
%update_maven_depmap

%postun
%update_maven_depmap

%files
%defattr(-,root,root,-)
%{_javadir}/*
%{_mavenpomdir}/*
%{_mavendepmapfragdir}/*

%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/%{name}

%changelog
* Wed Jan 19 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.3.2-1
- Update to latest version (2.3.2)
- Modifications according to new guidelines
- Build with maven 3

* Wed May 12 2010 Alexander Kurtakov <akurtako@redhat.com> 2.0.2-2
- Add missing requires.

* Tue May 11 2010 Alexander Kurtakov <akurtako@redhat.com> 2.0.2-1
- Initial package.
