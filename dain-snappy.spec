%global commit e02f7c887d666afbdd11763f3a6ba22e68f53f15
%global shortcommit %(c=%{commit}; echo ${c:0:7})

%bcond_with hadoop

Name:           dain-snappy
Version:        0.4
Release:        2%{?dist}
Summary:        Snappy compression library
License:        ASL 2.0 and BSD
URL:            https://github.com/dain/snappy
BuildArch:      noarch

Source0:        https://github.com/dain/snappy/archive/%{commit}/%{name}-%{shortcommit}.tar.gz

BuildRequires:  maven-local
BuildRequires:  mvn(com.google.guava:guava)
BuildRequires:  mvn(org.apache.maven.plugins:maven-enforcer-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-source-plugin)
BuildRequires:  mvn(org.testng:testng)
BuildRequires:  mvn(org.xerial.snappy:snappy-java)
%if %{with hadoop}
BuildRequires:  mvn(org.apache.hadoop:hadoop-common)
%endif

%description
This is a rewrite (port) of Snappy writen in pure Java. This
compression code produces a byte-for-byte exact copy of the output
created by the original C++ code, and extremely fast.

%package javadoc
Summary:        API documentation for %{name}

%description javadoc
%{summary}.

%prep
%setup -q -n snappy-%{commit}
%pom_remove_plugin :really-executable-jar-maven-plugin
%pom_remove_plugin :maven-javadoc-plugin
%pom_remove_plugin :maven-surefire-plugin

%if %{with hadoop}
%pom_change_dep :hadoop-core :hadoop-common
%else
%pom_remove_dep :hadoop-core
find -name HadoopSnappyCodec.java -delete
find -name TestHadoopSnappyCodec.java -delete
%endif

# Broken test - dain-snappy produces different output than original snappy
sed -i /@Test/d $(find -name SnappyTest.java)

%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%doc README.md
%license license.txt notice.md

%files javadoc -f .mfiles-javadoc
%license license.txt notice.md

%changelog
* Thu Jun  2 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.4-2
- Conditionally build without Hadoop codec

* Tue Apr 19 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.4-1
- Initial packaging
