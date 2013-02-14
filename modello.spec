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

Name:           modello
Version:        1.5
Release:        7%{?dist}
Epoch:          0
Summary:        Modello Data Model toolkit
License:        ASL 2.0 and BSD and MIT
Group:          Development/Libraries
URL:            http://modello.codehaus.org/
Source0:        http://repo2.maven.org/maven2/org/codehaus/%{name}/%{name}/%{version}/%{name}-%{version}-source-release.zip
Source1:        http://www.apache.org/licenses/LICENSE-2.0.txt
Source2:        %{name}-jpp-depmap.xml


BuildArch:      noarch

BuildRequires:  ant >= 0:1.6
BuildRequires:  jpackage-utils >= 0:1.7.2
BuildRequires:  maven-local
BuildRequires:  maven-assembly-plugin
BuildRequires:  maven-compiler-plugin
BuildRequires:  maven-install-plugin
BuildRequires:  maven-jar-plugin
BuildRequires:  maven-javadoc-plugin
BuildRequires:  maven-project
BuildRequires:  maven-resources-plugin
BuildRequires:  maven-surefire-plugin
BuildRequires:  maven-site-plugin
BuildRequires:  maven-surefire-provider-junit
BuildRequires:  maven-dependency-plugin
BuildRequires:  maven-plugin-plugin
BuildRequires:  maven-shared-reporting-impl
BuildRequires:  maven-shared-invoker
BuildRequires:  classworlds >= 0:1.1
BuildRequires:  plexus-container-default
BuildRequires:  plexus-utils
BuildRequires:  plexus-velocity
BuildRequires:  velocity
BuildRequires:  maven-doxia
BuildRequires:  maven-doxia-sitetools
BuildRequires:  maven-doxia-tools
BuildRequires:  plexus-build-api
BuildRequires:  ws-jaxme
BuildRequires:  xmlunit
BuildRequires:  geronimo-parent-poms

Requires:       classworlds >= 0:1.1
Requires:       maven
Requires:       maven-project
Requires:       plexus-containers-container-default
Requires:       plexus-build-api
Requires:       plexus-utils
Requires:       plexus-velocity
Requires:       velocity
Requires:       guava
Requires:       xbean
Requires:       jpackage-utils

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
Group:          Documentation
Requires:       jpackage-utils

%description javadoc
API documentation for %{name}.

%prep
%setup -q 
cp -p %{SOURCE1} LICENSE

%build

# skip tests because we have too old xmlunit in Fedora now (1.0.8)
mvn-rpmbuild \
        -Dmaven.local.depmap.file=%{SOURCE2} \
        -Dmaven.test.skip=true \
        install javadoc:aggregate

%install
# poms and depmap fragments
install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}
for i in `find . -name pom.xml -not -path ./pom.xml -not -path "*src/it/*"`; do
    # i is in format ..../artifactid/pom.xml
    cp -p $i $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.`basename \`dirname $i\``.pom

    artifactname=`basename \`dirname $i\` | sed -e s:^modello-::g`
    %add_to_maven_depmap org.codehaus.modello modello-$artifactname %{version} JPP/%{name} $artifactname
done

cp -p pom.xml $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.modello-modello.pom
%add_maven_depmap JPP.modello-modello.pom

# script
install -d -m 755 $RPM_BUILD_ROOT%{_bindir}
%jpackage_script org.codehaus.modello.ModelloCli "" ""  "modello/core:modello/plugin-xpp3:modello/plugin-xml:guava:xbean:plexus/containers-container-default:plexus/utils:plexus/classworlds)" %{name} true

# jars

install -d -m 755 $RPM_BUILD_ROOT%{_javadir}/%{name}
for jar in $(find -type f -name "*-%{version}.jar" | grep -E target/.*.jar); do
        install -m 644 $jar $RPM_BUILD_ROOT%{_javadir}/%{name}/`basename $jar |sed -e s:modello-::g|sed -e s:-%{version}::g`
done

# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -pr target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}

%files
%doc LICENSE
%{_mavenpomdir}/*
%{_javadir}/%{name}
%{_bindir}/*
%{_mavendepmapfragdir}/*

%files javadoc
%doc LICENSE
%{_javadocdir}/%{name}

%changelog
* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 0:1.5-6
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Thu Nov 15 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.5-5
- Add JPP depmap for maven-project to override versionless depmap
- Add missing BR/R: maven-project
- Remove unneeded BR: jpa_api

* Thu Nov 15 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.5-4
- Fix license tag
- Install text of Apache license

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Aug 8 2011 Alexander Kurtakov <akurtako@redhat.com> 0:1.5-1
- Update to upstream 1.5.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 26 2011 Alexander Kurtakov <akurtako@redhat.com> 0:1.4.1-1
- Update to upstream 1.4.1.

* Wed Dec  1 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.4-3
- Fix pom filenames (remove poms of integration tests) Resolves rhbz#655818
- Use jpackage_script macro to generate script

* Thu Aug 26 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.4-2
- Remove dtdparser BR/R

* Tue Jul 20 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.4-1
- Update to latest upstream version
- Re-enable javadoc generation
- Remove old workarounds/patches

* Mon May 24 2010 Yong Yang <yyang@redhat.com> 1.1-2
- Fix JPP pom name
- Disable javadoc:javadoc due to the failure of maven-doxia

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
