Name:           plexus-io
Version:        1.0
Release:        0.3.a5%{?dist}
Summary:        Plexus IO Components

Group:          Development/Libraries
License:        ASL 2.0
URL:            http://plexus.codehaus.org/plexus-components/plexus-io
#svn export http://svn.codehaus.org/plexus/plexus-components/tags/plexus-io-1.0-alpha-5/
#tar cjf plexus-io-1.0-alpha-5.tar.bz2 plexus-io-1.0-alpha-5/      
Source0:        plexus-io-1.0-alpha-5.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch: noarch

BuildRequires: java-devel >= 1:1.6.0 
BuildRequires:  jpackage-utils

BuildRequires: plexus-utils
BuildRequires: plexus-container-default
BuildRequires: maven2
BuildRequires: maven2-plugin-resources
BuildRequires: maven2-plugin-compiler
BuildRequires: maven2-plugin-jar
BuildRequires: maven2-plugin-install
BuildRequires: maven2-plugin-javadoc
BuildRequires: maven-surefire-maven-plugin
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

%description javadoc
API documentation for %{name}.


%prep
%setup -q -n %{name}-1.0-alpha-5

mkdir external_repo
ln -s %{_javadir} external_repo/JPP

%build
export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mvn-jpp \
        -e \
        -Dmaven2.jpp.mode=true \
        -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
        install javadoc:javadoc

%install
rm -rf %{buildroot}

# jars
install -d -m 0755 %{buildroot}%{_javadir}/plexus
install -m 644 target/%{name}-1.0-alpha-5.jar   %{buildroot}%{_javadir}/plexus/io-1.0.jar

(cd %{buildroot}%{_javadir}/plexus && for jar in *-%{version}*; \
    do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

%add_to_maven_depmap org.codehaus.plexus %{name} %{version} JPP/plexus io

# poms
install -d -m 755 %{buildroot}%{_datadir}/maven2/poms
install -pm 644 pom.xml \
    %{buildroot}%{_datadir}/maven2/poms/JPP.%{name}.pom

# javadoc
install -d -m 0755 %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -pr target/site/api*/* %{buildroot}%{_javadocdir}/%{name}-%{version}/
ln -s %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}
rm -rf target/site/api*

%post
%update_maven_depmap

%postun
%update_maven_depmap

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc NOTICE.txt
%{_javadir}/plexus/*.jar
%{_datadir}/maven2/poms/*
%{_mavendepmapfragdir}/*

%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}

%changelog
* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.3.a5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 23 2009 Alexander Kurtakov <akurtako@redhat.com> 1.0-0.2.a5
- Fix review comments.

* Wed Dec 23 2009 Alexander Kurtakov <akurtako@redhat.com> 1.0-0.1.a5.1
- Initial package
