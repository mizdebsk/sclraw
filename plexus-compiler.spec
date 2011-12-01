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
%global dirhash a7f8290
%global githash 7ca7d76

Name:       plexus-compiler
Version:    1.8
Release:    3%{?dist}
Epoch:      0
Summary:    Compiler call initiators for Plexus
License:    MIT
Group:      Development/Java
URL:        http://plexus.codehaus.org/

# wget  https://nodeload.github.com/sonatype/plexus-components/tarball/plexus-compiler-1.8
Source0:    sonatype-plexus-components-%{name}-%{version}-0-g%{githash}.tar.gz

Patch0:     0001-Remove-aspecj-support.patch

BuildArch:      noarch
BuildRequires:  maven
BuildRequires:  jpackage-utils
BuildRequires:  junit
BuildRequires:  classworlds
BuildRequires:  eclipse-ecj
BuildRequires:  plexus-container-default
BuildRequires:  plexus-utils
BuildRequires:  plexus-containers-component-metadata

Requires:       classworlds
Requires:       plexus-container-default
Requires:       plexus-utils

%description
Plexus Compiler adds support for using various compilers from a
unified api. Support for javac is available in main package. For
additional compilers see %{name}-extras package.

%package extras
Summary:        Extra compiler support for %{name}
Group:          Development/Libraries
Requires:       jpackage-utils
Requires:       eclipse-ecj
Requires:       %{name} = %{version}-%{release}

%description extras
Additional support for csharp, eclipse and jikes compilers

%package javadoc
Summary:        Javadoc for %{name}
Group:          Documentation
Requires:       jpackage-utils

%description javadoc
API documentation for %{name}.

%prep
%setup -q -n sonatype-plexus-components-%{dirhash}
%patch0 -p1


# don't build/install compiler-test module, it needs maven2 test harness
sed -i 's:<module>plexus-compiler-test</module>::' pom.xml

%build
mvn-rpmbuild -e \
        -Dmaven.test.skip=true \
        install javadoc:aggregate


%install
# jars
install -d -m 755 %{buildroot}%{_javadir}/%{parent}
install -d -m 755 %{buildroot}%{_mavenpomdir}

for mod in plexus-compiler-{api,manager}; do
    jarname=${mod/plexus-}
    install -pm 644 $mod/target/${mod}-%{version}.jar \
                    %{buildroot}%{_javadir}/%{parent}/$jarname.jar

    install -pm 644 $mod/pom.xml %{buildroot}%{_mavenpomdir}/JPP.%{parent}-$jarname.pom
    %add_maven_depmap JPP.%{parent}-$jarname.pom %{parent}/$jarname.jar
done

pushd plexus-compilers
for mod in plexus-compiler-{csharp,eclipse,jikes,javac}; do
    jarname=${mod/plexus-}
    install -pm 644 $mod/target/${mod}-%{version}.jar \
                    %{buildroot}%{_javadir}/%{parent}/$jarname.jar

    install -pm 644 $mod/pom.xml %{buildroot}%{_mavenpomdir}/JPP.%{parent}-$jarname.pom
    %add_maven_depmap JPP.%{parent}-$jarname.pom %{parent}/$jarname.jar -f extras
done

install -pm 644 plexus-compiler-javac/target/plexus-compiler-javac-%{version}.jar \
                    %{buildroot}%{_javadir}/%{parent}/compiler-javac.jar

install -pm 644 plexus-compiler-javac/pom.xml %{buildroot}%{_mavenpomdir}/JPP.%{parent}-compiler-javac.pom
%add_maven_depmap JPP.%{parent}-compiler-javac.pom %{parent}/compiler-javac.jar

install -pm 644 pom.xml %{buildroot}%{_mavenpomdir}/JPP.%{parent}-compilers.pom
%add_maven_depmap JPP.%{parent}-compilers.pom
popd

install -pm 644 pom.xml %{buildroot}%{_mavenpomdir}/JPP.%{parent}-compiler.pom
%add_maven_depmap JPP.%{parent}-compiler.pom


# javadocs
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -pr target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}

%pre javadoc
# workaround for rpm bug, can be removed in F-17
[ $1 -gt 1 ] && [ -L %{_javadocdir}/%{name} ] && \
rm -rf $(readlink -f %{_javadocdir}/%{name}) %{_javadocdir}/%{name} || :


%files
%{_javadir}/%{parent}/compiler-api.jar
%{_javadir}/%{parent}/compiler-manager.jar
%{_javadir}/%{parent}/compiler-javac.jar
%{_mavenpomdir}/JPP.%{parent}-compilers.pom
%{_mavenpomdir}/JPP.%{parent}-compiler.pom
%{_mavenpomdir}/JPP.%{parent}-compiler-api.pom
%{_mavenpomdir}/JPP.%{parent}-compiler-manager.pom
%{_mavenpomdir}/JPP.%{parent}-compiler-javac.pom
%{_mavendepmapfragdir}/%{name}

%files extras
%{_mavendepmapfragdir}/%{name}-extras
%{_javadir}/%{parent}/compiler-csharp.jar
%{_javadir}/%{parent}/compiler-eclipse.jar
%{_javadir}/%{parent}/compiler-jikes.jar
%{_mavenpomdir}/JPP.%{parent}-compiler-jikes.pom
%{_mavenpomdir}/JPP.%{parent}-compiler-eclipse.pom
%{_mavenpomdir}/JPP.%{parent}-compiler-csharp.pom

%files javadoc
%doc %{_javadocdir}/%{name}

%changelog
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

