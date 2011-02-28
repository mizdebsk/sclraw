# Copyright (c) 2000-2007, JPackage Project
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

%global parent plexus
%global subname utils

Name:           plexus-utils
Version:        2.0.6
Release:        1%{?dist}
Summary:        Plexus Common Utilities
License:        ASL 1.1 and ASL 2.0 and MIT
Group:          Development/Libraries
URL:            http://plexus.codehaus.org/
# git clone git://github.com/sonatype/sisu
# git archive --prefix="plexus-utils-2.0.6/" --format=tar plexus-utils-2.0.6 | bzip2 > plexus-utils-2.0.6.tar.bz2
Source0:        plexus-utils-%{version}.tar.bz2

BuildArch:      noarch
BuildRequires:  jpackage-utils >= 0:1.6
Requires:       jpackage-utils
Requires(postun): jpackage-utils

BuildRequires:  maven2
BuildRequires:  maven-compiler-plugin
BuildRequires:  maven-install-plugin
BuildRequires:  maven-jar-plugin
BuildRequires:  maven-javadoc-plugin
BuildRequires:  maven-resources-plugin
BuildRequires:  maven-surefire-plugin
BuildRequires:  maven-doxia-sitetools
BuildRequires:  maven-surefire-provider-junit

Requires(post):    jpackage-utils >= 0:1.7.2
Requires(postun):  jpackage-utils >= 0:1.7.2

%description
The Plexus project seeks to create end-to-end developer tools for
writing applications. At the core is the container, which can be
embedded or for a full scale application server. There are many
reusable components for hibernate, form processing, jndi, i18n,
velocity, etc. Plexus also includes an application server which
is like a J2EE application server, without all the baggage.

%package javadoc
Summary:          Javadoc for %{name}
Group:            Documentation
Requires:         jpackage-utils
Requires(postun): jpackage-utils

%description javadoc
Javadoc for %{name}.

%prep
%setup -q

%build
mvn-rpmbuild install javadoc:javadoc

%install
# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}/%{parent}
install -pm 644 target/%{name}-%{version}.jar \
  $RPM_BUILD_ROOT%{_javadir}/plexus/utils.jar

# pom
install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -pm 644 pom.xml $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{parent}-%{subname}.pom

%add_to_maven_depmap org.codehaus.plexus %{name} %{version} JPP/%{parent} %{subname}
# compatibility depmap
%add_to_maven_depmap plexus %{name} %{version} JPP/%{parent} %{subname}

# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -pr target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}

%post
%update_maven_depmap

%postun
%update_maven_depmap

%pre javadoc
# workaround for rpm bug, can be removed in F-17
[ $1 -gt 1 ] && [ -L %{_javadocdir}/%{name} ] && \
rm -rf $(readlink -f %{_javadocdir}/%{name}) %{_javadocdir}/%{name} || :

%files
%defattr(-,root,root,-)
%{_javadir}/*
%{_mavenpomdir}/*
%{_mavendepmapfragdir}/*

%files javadoc
%defattr(-,root,root,-)
%doc %{_javadocdir}/%{name}

%changelog
* Mon Feb 28 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.0.6-1
- Update to 2.0.6
- Remove obsolete patches
- Use maven 3 to build

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.0.5-2
- Use versionless jars/javadocs
- Use new maven plugin names
- Add compatibility depmap

* Wed May  5 2010 Mary Ellen Foster <mefoster at gmail.com> 2.0.5-1
- Update to 2.0.5

* Fri Feb 12 2010 Mary Ellen Foster <mefoster at gmail.com> 2.0.1-1
- Update to 2.0.1
- Build with maven

* Wed Aug 19 2009 Andrew Overholt <overholt@redhat.com> 1.4.5-1.2
- Update to 1.4.5 from JPackage and Deepak Bhole
- Remove gcj bits

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.2-4.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.2-3.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:1.2-2.2
- fix license tag
- drop repotag

* Thu Aug 23 2007 Ralph Apel <r.apel@r-apel.de> - 0:1.4.5-1jpp
- Upgrade to 1.4.5
- Now build with maven2 by default

* Wed Mar 21 2007 Ralph Apel <r.apel@r-apel.de> - 0:1.2-2jpp
- Fix build classpath
- Optionally build with maven2
- Add gcj_support option

* Mon Feb 20 2007 Deepak Bhole <dbhole@redhat.com> - 0:1.2-2jpp.1.fc7
- Fix spec per Fedora guidelines

* Fri Jun 16 2006 Ralph Apel <r.apel@r-apel.de> - 0:1.2-1jpp
- Upgrade to 1.2

* Wed Jan 04 2006 Fernando Nasser <fnasser@redhat.com> - 0:1.0.4-2jpp
- First JPP 1.7 build

* Mon Nov 07 2005 Ralph Apel <r.apel at r-apel.de> - 0:1.0.4-1jpp
- First JPackage build
