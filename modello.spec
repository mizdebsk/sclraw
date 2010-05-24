# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define _without_gcj_support 1
%define gcj_support %{?_with_gcj_support:1}%{!?_with_gcj_support:%{?_without_gcj_support:0}%{!?_without_gcj_support:%{?_gcj_support:%{_gcj_support}}%{!?_gcj_support:0}}}


%define repo_dir    .m2/repository

%define namedversion 1.1
%define maven_settings_file %{_builddir}/%{name}-%{namedversion}/settings.xml

Name:           modello
Version:        1.1
Release:        1%{?dist}
Epoch:          0
Summary:        Modello Data Model toolkit
License:        MIT  
Group:          Development/Java
URL:            http://modello.codehaus.org/
Source0:        %{name}-%{namedversion}-src.tar.gz
# svn export https://svn.codehaus.org/modello/tags/modello-1.0.1/
# tar czf modello-1.0.1-src.tar.gz modello-1.0.1/
Source1:        modello.script

Source2:                %{name}-jpp-depmap.xml

#Patch0:                 modello-hibernateold-artifactid-fix.patch
#Patch1:                 modello-build-all-plugins.patch
#Patch2:                 modello-use-old-pdcontainer.patch
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  ant >= 0:1.6
BuildRequires:  jpackage-utils >= 0:1.7.2
BuildRequires:  maven2 >= 2.0.4-9
BuildRequires:  maven2-plugin-assembly
BuildRequires:  maven2-plugin-compiler
BuildRequires:  maven2-plugin-install
BuildRequires:  maven2-plugin-jar
BuildRequires:  maven-javadoc-plugin
BuildRequires:  maven2-plugin-resources
BuildRequires:  maven2-plugin-surefire
BuildRequires:  maven-site-plugin
BuildRequires:  maven-surefire-provider-junit
BuildRequires:  maven2-plugin-plugin
BuildRequires:  maven-shared-reporting-impl
BuildRequires:  classworlds >= 0:1.1
BuildRequires:  dtdparser
BuildRequires:  plexus-container-default
BuildRequires:  plexus-utils
BuildRequires:  plexus-velocity
BuildRequires:  velocity
BuildRequires:  maven-doxia
BuildRequires:  maven-doxia-sitetools
BuildRequires:  maven-doxia-tools
BuildRequires:  tomcat5
BuildRequires:  plexus-build-api

Requires:       classworlds >= 0:1.1
Requires:       dtdparser
Requires:       plexus-container-default
Requires:       plexus-utils
Requires:       plexus-velocity
Requires:       velocity

Requires:          jpackage-utils >= 0:1.7.2
Requires(post):    jpackage-utils >= 0:1.7.2
Requires(postun):  jpackage-utils >= 0:1.7.2

Provides:       modello-maven-plugin = %{epoch}:%{version}-%{release}
Obsoletes:      modello-maven-plugin < 0:1.0-0.a8.3jpp

%description
Modello is a Data Model toolkit in use by the 
http://maven.apache.org/maven2.
It all starts with the Data Model. Once a data model is defined, 
the toolkit can be used to generate any of the following at compile 
time.
Java POJOs of the model.
Java POJOs to XML Writer (provided via xpp3 or dom4j).
XML to Java Pojos Reader (provided via xpp3 or dom4j).
XDoc documentation of the data model.
Java model to [Prevayler|http://www.prevayler.org/] Store.
Java model to [JPOX|http://www.jpox.org/] Store.
Java model to [JPOX|http://www.jpox.org/] Mapping.


%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Documentation

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -n %{name}-%{namedversion}
#%patch0 -b .sav
#%patch1 -b .sav
#%patch2 -b .sav

find . -name release-pom.xml -exec rm -f '{}' \;

#Fixme: got error of Unrecognised tag: 'menu'
find . -name site.xml -exec rm -f '{}' \;

#for i in modello-plugins-sandbox/modello-plugin-ldap/src/test/java/org/codehaus/modello/plugin/ldap/ObjStateFactoryModelloGeneratorTest.java \
#         modello-plugins-sandbox/modello-plugin-ldap/src/test/java/org/codehaus/modello/plugin/ldap/LdapSchemaGeneratorTest.java \
#         modello-plugins-sandbox/modello-plugin-ojb/src/test/java/org/codehaus/modello/plugin/ojb/OjbModelloGeneratorTest.java \
#         modello-plugins-sandbox/modello-plugin-stash/src/test/java/org/codehaus/modello/plugin/stash/StashModelloGeneratorTest.java \
#         modello-plugins-sandbox/modello-plugin-hibernate-store/src/test/java/org/codehaus/modello/plugin/hibernate/HibernateModelloGeneratorTest.java; do
#        sed -i -e s:org.codehaus.modello.ModelloGeneratorTest:org.codehaus.modello.AbstractModelloGeneratorTest:g $i
#        sed -i -e s:"extends ModelloGeneratorTest":"extends AbstractModelloGeneratorTest":g $i
#done

%build

export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mkdir -p $MAVEN_REPO_LOCAL

mvn-jpp \
        -e \
        -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
        -Dmaven2.jpp.depmap.file=%{SOURCE2} \
        -Dmaven.test.failure.ignore=true \
        -Dmaven.test.skip=true \
        install

# Manual iteration should not be needed, but there is a bug in the javadoc 
# plugin which makes this necessary. See: 
# http://jira.codehaus.org/browse/MJAVADOC-157
for dir in modello-*; do
    pushd $dir
        mvn-jpp \
          -e \
          -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
          -Dmaven2.jpp.depmap.file=%{SOURCE2} \
          -Dmaven.test.failure.ignore=true \
          javadoc:javadoc
    popd
done

for dir in modello-plugins/modello-plugin-*; do
    pushd $dir
        mvn-jpp \
          -e \
          -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
          -Dmaven2.jpp.depmap.file=%{SOURCE2} \
          -Dmaven.test.failure.ignore=true \
          javadoc:javadoc
    popd
done

%install
rm -rf $RPM_BUILD_ROOT

# poms
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/maven2/poms
for i in `find . -name pom.xml | grep -v \\\./pom.xml`; do
        cp -p $i $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP-`basename \`dirname $i\``.pom
done

# Depmap fragments
for i in `find . -name pom.xml | grep -v \\\./pom.xml |  grep -v modello-plugins-sandbox`; do
    # i is in format ..../artifactid/pom.xml
    artifactname=`basename \`dirname $i\` | sed -e s:^modello-::g`

    %add_to_maven_depmap org.codehaus.modello modello-$artifactname %{namedversion} JPP/%{name} $artifactname
done

cp -p pom.xml $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP-modello-modello.pom
%add_to_maven_depmap org.codehaus.modello modello %{namedversion} JPP/%{name} modello

# script
install -d -m 755 $RPM_BUILD_ROOT%{_bindir}
install -m 755 %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/%{name}

# jars

ls -lR

install -d -m 755 $RPM_BUILD_ROOT%{_javadir}/%{name}
for jar in $(find -type f -name "*.jar" | grep -E target/.*.jar); do 
        install -m 644 $jar $RPM_BUILD_ROOT%{_javadir}/%{name}/`basename $jar |sed -e s:modello-::g`
done

(cd $RPM_BUILD_ROOT%{_javadir}/%{name} && for jar in *-%{namedversion}*; do ln -sf ${jar} `echo $jar| sed  "s|-%{namedversion}||g"`; done)

# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
for target in $(find -type d -name target); do
  if [ -d $target/site/apidocs ]; then
    install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/`basename \`dirname $target\` | sed -e s:modello-::g`
    cp -pr $target/site/apidocs/* $jar $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/`basename \`dirname $target\` | sed -e s:modello-::g`
  fi
done
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_maven_depmap

%postun
%update_maven_depmap

%files
%defattr(-,root,root,-)
%{_datadir}/maven2
%{_javadir}/%{name}
%attr(755,root,root) %{_bindir}/*
%{_mavendepmapfragdir}

%files javadoc
%defattr(-,root,root,-)
%doc %{_javadocdir}/*

%changelog
* Mon May 24 2010 Yong Yang <yyang@redhat.com> 1.1-1
- Upgrade to 1.1

* Fri May 21 2010 Yong Yang <yyang@redhat.com> 1.0.1-1
- Upgrade to 1.0.1

* Thu Aug 20 2009 Andrew Overholt <overholt@redhat.com> 1.0-0.4.a15.0.1
- Update to alpha 15 courtesy Deepak Bhole

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-0.3.a8.4.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-0.2.a8.4.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:1.0-0.1.a8.4.4
- drop repotag

* Tue Mar 20 2007 Matt Wringe <wringe@redhat.com> 0:1.0-0.1.a8.4jpp.3
- disable gcj support

* Tue Mar 13 2007 Matt Wringe <mwringe@redhat.com> 0:1.0-0.1.a8.4jpp.2
- Change license to MIT to reflex the actual license specified in the
  source headers.
- fix various rpmlint issues 

* Mon Feb 26 2007 Tania Bento <tbento@redhat.com> 0:1.0-0.1.a8.4jpp.1
- Fixed %%Release.
- Fixed %%License.
- Fixed %%BuildRoot.
- Removed %%Vendor.
- Removed %%Distribution.
- Defined _with_gcj_support and gcj_support.
- Fixed instructions on how to generate the source drop.

* Fri Dec 01 2006 Deepak Bhole <dbhole@redhat.com> 1.0-0.a8.4jpp
- Added an obsoletes for older versions of the plugin

* Thu Oct 19 2006 Deepak Bhole <dbhole@redhat.com> 1.0-0.a8.3jpp
- Update for maven2 9jpp
- Merge maven-plugin subpackage into the main one

* Mon Sep 11 2006 Ralph Apel <r.apel at r-apel.de> - 0:1.0-0.a8.2jpp
- Add gcj_support option
- Add post/postun Requires for javadoc
- Don't omit maven-plugin upload

* Fri Jun 23 2006 Deepak Bhole <dbhole@redhat.com> - 0:1.0-0.a8.1jpp
- Upgrade to 1.0-alpha-8
- Remove ant build, add maven2 build

* Thu Jun 01 2006 Fernando Nasser <fnasser@redhat.com> - 0:1.0-0.a4.2jpp
- First JPP 1.7 build

* Mon Nov 07 2005 Ralph Apel <r.apel at r-apel.de> - 0:1.0-0.a4.1jpp
- First JPackage build

