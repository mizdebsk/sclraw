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

%global parent  plexus
%global dirhash 16e340d

Name:       plexus-compiler
Version:    2.1
Release:    1%{?dist}
Epoch:      0
Summary:    Compiler call initiators for Plexus
# extras subpackage has a bit different licensing
# parts of compiler-api are ASL2.0/MIT
License:    MIT and ASL 2.0
Group:      Development/Java
URL:        http://plexus.codehaus.org/

Source0:    https://github.com/sonatype/%{name}/tarball/%{name}-%{version}#/%{name}-%{version}.tar.gz
Patch0:     0001-change-artifactIds.patch

BuildArch:      noarch
BuildRequires:  maven-local
BuildRequires:  jpackage-utils
BuildRequires:  junit
BuildRequires:  classworlds
BuildRequires:  plexus-compiler-extras
BuildRequires:  eclipse-ecj
BuildRequires:  plexus-containers-container-default
BuildRequires:  plexus-utils
BuildRequires:  plexus-containers-component-metadata
BuildRequires:  junit4
BuildRequires:  plexus-pom

%description
Plexus Compiler adds support for using various compilers from a
unified api. Support for javac is available in main package. For
additional compilers see %{name}-extras package.

%package extras
Summary:        Extra compiler support for %{name}
# ASL 2.0: src/main/java/org/codehaus/plexus/compiler/util/scan/
#          ...codehaus/plexus/compiler/csharp/CSharpCompiler.java
# ASL 1.1/MIT: ...codehaus/plexus/compiler/jikes/JikesCompiler.java
License:        MIT and ASL 2.0 and ASL 1.1

%description extras
Additional support for csharp, eclipse and jikes compilers

%package pom
Summary:        Maven POM files for %{name}

%description pom
This package provides %{summary}.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Documentation

%description javadoc
API documentation for %{name}.

%prep
%setup -q -n sonatype-plexus-compiler-%{dirhash}

%patch0 -p1

%pom_disable_module plexus-compiler-aspectj plexus-compilers/pom.xml

# don't build/install compiler-test module, it needs maven2 test harness
%pom_disable_module plexus-compiler-test

%build
%mvn_package ":plexus-compiler-temp" pom
%mvn_package ":plexus-compilers-temp" pom
%mvn_package ":*{csharp,eclipse,jikes}*" extras
# Tests are skipped because of unavailable plexus-compiler-test artifact
%mvn_build -f

%install
%mvn_install

# only temporary solution
# we need to preserve older JARs and POMs for a while, because current maven-compiler-plugin
# won't work with this newer version of plexus-compiler and we can't update maven-compiler-plugin
# because it requires this newer version of plexus-compiler.
# thus temporarly we need both versions of plexus-compiler
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}/plexus
cp /usr/share/java/plexus/compiler-api.jar     %{buildroot}/usr/share/java/plexus/compiler-api.jar
cp /usr/share/java/plexus/compiler-javac.jar   %{buildroot}/usr/share/java/plexus/compiler-javac.jar
cp /usr/share/java/plexus/compiler-manager.jar %{buildroot}/usr/share/java/plexus/compiler-manager.jar
cp /usr/share/java/plexus/compiler-csharp.jar  %{buildroot}/usr/share/java/plexus/compiler-csharp.jar
cp /usr/share/java/plexus/compiler-eclipse.jar %{buildroot}/usr/share/java/plexus/compiler-eclipse.jar
cp /usr/share/java/plexus/compiler-jikes.jar   %{buildroot}/usr/share/java/plexus/compiler-jikes.jar
cp /usr/share/maven-poms/JPP.plexus-compiler-api.pom     %{buildroot}/usr/share/maven-poms/JPP.plexus-compiler-api.pom
cp /usr/share/maven-poms/JPP.plexus-compiler-javac.pom   %{buildroot}/usr/share/maven-poms/JPP.plexus-compiler-javac.pom
cp /usr/share/maven-poms/JPP.plexus-compiler-manager.pom %{buildroot}/usr/share/maven-poms/JPP.plexus-compiler-manager.pom
cp /usr/share/maven-poms/JPP.plexus-compiler-org.codehaus.plexus@plexus-compiler.pom %{buildroot}/usr/share/maven-poms/JPP.plexus-compiler-org.codehaus.plexus@plexus-compiler.pom
cp /usr/share/maven-poms/JPP.plexus-compiler-org.codehaus.plexus@plexus-compilers.pom %{buildroot}/usr/share/maven-poms/JPP.plexus-compiler-org.codehaus.plexus@plexus-compilers.pom
cp /usr/share/maven-poms/JPP.plexus-compiler-csharp.pom  %{buildroot}/usr/share/maven-poms/JPP.plexus-compiler-csharp.pom
cp /usr/share/maven-poms/JPP.plexus-compiler-eclipse.pom %{buildroot}/usr/share/maven-poms/JPP.plexus-compiler-eclipse.pom
cp /usr/share/maven-poms/JPP.plexus-compiler-jikes.pom   %{buildroot}/usr/share/maven-poms/JPP.plexus-compiler-jikes.pom
cp /usr/share/maven-fragments/plexus-compiler.xml %{buildroot}/usr/share/maven-fragments/plexus-compiler-orig.xml

%files -f .mfiles
%{_javadir}/plexus/*
%{_mavenpomdir}/*
%{_mavendepmapfragdir}/*
%files extras -f .mfiles-extras
%files pom -f .mfiles-pom

%files javadoc
%doc %{_javadocdir}/%{name}

%changelog
* Wed Jan 23 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.1-1
- Update to upstream version 2.1
- Build with xmvn

* Wed Dec 5 2012 Michal Srb <msrb@redhat.com> - 0:1.9.2-3
- Replaced dependency to plexus-container-default with plexus-containers-container-default

* Tue Nov 13 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.9.2-2
- Fix up licensing properly

* Mon Oct 29 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.9.2-1
- Update to upstream version 1.9.2

* Wed Aug  8 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.9.1-3
- Fix FTBFS by adding ignoreOptionalProblems function
- Use new pom_ macros instead of patches

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 19 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.9.1-1
- Update to upstream 1.9.1 release

* Fri Jan 13 2012 Alexander Kurtakov <akurtako@redhat.com> 0:1.8.3-1
- Update to upstream 1.8.3 release.
- For some reason junit is strong (not test) dependency.

* Thu Dec  1 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.8-3
- Build with maven 3
- Don't install compiler-test module (nothing should use it anyway)
- Fixes accoding to current guidelines
- Install depmaps into extras separately

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 20 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.8-1
- Update to latest version (1.8)
- Create extras subpackage with optional compilers
- Provide maven depmaps
- Versionless jars & javadocs

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.5.2-4.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.5.2-3.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:1.5.2-2.3
- drop repotag

* Thu Mar 15 2007 Deepak Bhole <dbhole@redhat.com> - 0:1.5.2-2jpp.2
- Fix bug in spec that prevented unversioned symlink creation

* Thu Mar 08 2007 Deepak Bhole <dbhole@redhat.com> - 0:1.5.2-2jpp.1
- Fix license
- Disable aspectj compiler until we can put that into Fedora
- Remove vendor and distribution tags
- Removed javadoc post and postuns, with dirs being marked %%doc now
- Fix buildroot per Fedora spec

* Fri Jun 02 2006 Ralph Apel <r.apel at r-apel.de> - 0:1.5.2-2jpp
- Fix jar naming to previous plexus conventions

* Tue May 30 2006 Ralph Apel <r.apel at r-apel.de> - 0:1.5.2-1jpp
- First JPackage build
