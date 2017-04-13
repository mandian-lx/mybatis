%{?_javapackages_macros:%_javapackages_macros}

# Started: Wed, 06 Jul 2016 13:50:35 UTC
# Terminated: Thu, 07 Jul 2016 06:37:46 UTC
%bcond_with test

Name:          mybatis
Version:       3.2.8
Release:       7%{?dist}
Summary:       SQL Mapping Framework for Java
Group:         Development/Java
License:       ASL 2.0
# http://code.google.com/p/mybatis/
URL:           http://www.mybatis.org/
Source0:       https://github.com/mybatis/mybatis-3/archive/%{name}-%{version}.tar.gz
# thanks to jhernand
# replace ognl ognl with apache-commons-ognl
Patch0:        %{name}-%{version}-commons-ognl.patch

Patch1:        mybatis-3.2.8-log4j2.6.patch

BuildRequires: maven-local
BuildRequires: mvn(cglib:cglib)
BuildRequires: mvn(commons-logging:commons-logging)
BuildRequires: mvn(log4j:log4j:1.2.17)
BuildRequires: mvn(org.apache.commons:commons-ognl)
BuildRequires: mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires: mvn(org.apache.logging.log4j:log4j-core)
BuildRequires: mvn(org.apache.maven.plugins:maven-enforcer-plugin)
BuildRequires: mvn(org.apache.maven.plugins:maven-site-plugin)
BuildRequires: mvn(org.javassist:javassist)
BuildRequires: mvn(org.mybatis:mybatis-parent:pom:)
BuildRequires: mvn(org.slf4j:slf4j-api)
BuildRequires: mvn(org.slf4j:slf4j-log4j12)

%if %{with test}
# test deps
BuildRequires: mvn(commons-dbcp:commons-dbcp)
BuildRequires: mvn(junit:junit)
BuildRequires: mvn(org.apache.derby:derby)
BuildRequires: mvn(org.apache.geronimo.specs:geronimo-jta_1.1_spec)
BuildRequires: mvn(org.apache.geronimo.specs:specs:pom:)
BuildRequires: mvn(org.apache.velocity:velocity)
BuildRequires: mvn(org.hsqldb:hsqldb)
BuildRequires: mvn(org.mockito:mockito-core)
BuildRequires: mvn(postgresql:postgresql)
%endif

BuildArch:     noarch

%description
The MyBatis data mapper framework makes it easier
to use a relational database with object-oriented
applications. MyBatis couples objects with stored
procedures or SQL statements using a XML descriptor
or annotations. Simplicity is the biggest advantage
of the MyBatis data mapper over object relational
mapping tools.

To use the MyBatis data mapper, you rely on your
own objects, XML, and SQL. There is little to
learn that you don't already know. With the
MyBatis data mapper, you have the full power of
both SQL and stored procedures at your fingertips. 

The MyBatis project is developed and maintained by
a team that includes the original creators of the
"iBATIS" data mapper. The Apache project was retired
and continued here.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -n %{name}-3-%{name}-%{version}

%patch0 -p1
%patch1 -p1

%pom_remove_plugin :maven-pdf-plugin
%pom_remove_plugin :jarjar-maven-plugin
%pom_remove_plugin :cobertura-maven-plugin

sed -i 's/\r//' LICENSE NOTICE

%if %{with test}
%pom_remove_dep javax.transaction:transaction-api
%pom_add_dep org.apache.geronimo.specs:geronimo-jta_1.1_spec::test

# Fails on java8
rm src/test/java/org/apache/ibatis/parsing/GenericTokenParserTest.java

rm src/test/java/org/apache/ibatis/submitted/multipleresultsetswithassociation/MultipleResultSetTest.java \
 src/test/java/org/apache/ibatis/submitted/includes/IncludeTest.java \
 src/test/java/org/apache/ibatis/submitted/resultmapwithassociationstest/ResultMapWithAssociationsTest.java \
 src/test/java/org/apache/ibatis/submitted/nestedresulthandler_association/NestedResultHandlerAssociationTest.java

rm src/test/java/org/apache/ibatis/logging/LogFactoryTest.java
%endif

%mvn_file :%{name} %{name}

%build
# Test suite skipped

%if %{without test}
opts="-f"
%endif
%mvn_build $opts -- -Dproject.build.sourceEncoding=UTF-8
 
%install
%mvn_install

%files -f .mfiles
%doc LICENSE NOTICE

%files javadoc -f .mfiles-javadoc
%doc LICENSE NOTICE

%changelog
* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Aug 25 2016 gil cattaneo <puntogil@libero.it> 3.2.8-6
- log4j 2.6.1 build fix

* Wed Jul 06 2016 gil cattaneo <puntogil@libero.it> 3.2.8-5
- disable test suite

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Feb 10 2015 gil cattaneo <puntogil@libero.it> 3.2.8-2
- introduce license macro

* Wed Dec 24 2014 gil cattaneo <puntogil@libero.it> 3.2.8-1
- update to 3.2.8

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 3.2.2-6
- Use Requires: java-headless rebuild (#1067528)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 05 2013 gil cattaneo <puntogil@libero.it> 3.2.2-4
- switch to XMvn
- minor changes to adapt to current guideline

* Sat May 11 2013 gil cattaneo <puntogil@libero.it> 3.2.2-3
- rebuilt with mybatis-parent

* Sun Apr 21 2013 gil cattaneo <puntogil@libero.it> 3.2.2-2
- rebuilt with mybatis-parent
- run test suite with hsqldb 1.x

* Sat Apr 20 2013 gil cattaneo <puntogil@libero.it> 3.2.2-1
- update to 3.2.2

* Fri Apr 20 2012 gil cattaneo <puntogil@libero.it> 3.1.1-1
- initial rpm
