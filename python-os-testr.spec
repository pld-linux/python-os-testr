#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	A testr wrapper to provide functionality for OpenStack projects
Summary(pl.UTF-8):	Obudowanie testr dostarczające funkcjonalność dla projektów OpenStack
Name:		python-os-testr
# keep 1.x here for python2 support
Version:	1.1.0
Release:	2
License:	Apache v2.0
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/os-testr/
Source0:	https://files.pythonhosted.org/packages/source/o/os-testr/os-testr-%{version}.tar.gz
# Source0-md5:	8a470f96783c546075cf2a6ba0573431
Patch0:		os-testr-mock.patch
Patch1:		os-testr-subunit.patch
URL:		https://pypi.org/project/os-testr/
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-pbr >= 3.0.0
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-ddt >= 1.0.1
BuildRequires:	python-mock
BuildRequires:	python-oslotest >= 3.2.0
BuildRequires:	python-six >= 1.10.0
BuildRequires:	python-stestr >= 1.0.0
BuildRequires:	python-subunit >= 1.0.0
BuildRequires:	python-testscenarios >= 0.4
BuildRequires:	python-testtools >= 2.2.0
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.6
BuildRequires:	python3-pbr >= 3.0.0
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-ddt >= 1.0.1
BuildRequires:	python3-oslotest >= 3.2.0
BuildRequires:	python3-six >= 1.10.0
BuildRequires:	python3-stestr >= 1.0.0
BuildRequires:	python3-subunit >= 1.0.0
BuildRequires:	python3-testscenarios >= 0.4
BuildRequires:	python3-testtools >= 2.2.0
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python-openstackdocstheme >= 1.18.1
BuildRequires:	python-reno >= 2.5.0
BuildRequires:	sphinx-pdg-2 >= 1.7.0
%endif
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A testr wrapper to provide functionality for OpenStack projects.

%description -l pl.UTF-8
Obudowanie testr dostarczające funkcjonalność dla projektów OpenStack.

%package -n python3-os-testr
Summary:	A testr wrapper to provide functionality for OpenStack projects
Summary(pl.UTF-8):	Obudowanie testr dostarczające funkcjonalność dla projektów OpenStack
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.6

%description -n python3-os-testr
A testr wrapper to provide functionality for OpenStack projects.

%description -n python3-os-testr -l pl.UTF-8
Obudowanie testr dostarczające funkcjonalność dla projektów OpenStack.

%package apidocs
Summary:	API documentation for Python os-testr module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona os-testr
Group:		Documentation

%description apidocs
API documentation for Python os-testr module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona os-testr.

%prep
%setup -q -n os-testr-%{version}
%patch -P 0 -p1
%patch -P 1 -p1

%build
%if %{with python2}
%py_build

%if %{with tests}
install -d build-2/bin
ln -sf %{__python} build-2/bin/python
ln -sf %{_bindir}/stestr-2 build-2/bin/stestr
cp -p os_testr/ostestr.py build-2/bin/ostestr
%{__sed} -i -e '1s,/usr/bin/env python2,%{__python},' build-2/bin/ostestr
cp -p os_testr/subunit_trace.py build-2/bin/subunit-trace
%{__sed} -i -e '1s,/usr/bin/env python,%{__python},' build-2/bin/subunit-trace
PATH=$(pwd)/build-2/bin:$PATH \
PYTHONPATH=$(pwd) \
%{__python} os_testr/ostestr.py
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
install -d build-3/bin
ln -sf %{__python3} build-3/bin/python
ln -sf %{_bindir}/stestr-3 build-3/bin/stestr
cp -p os_testr/ostestr.py build-3/bin/ostestr
%{__sed} -i -e '1s,/usr/bin/env python2,%{__python3},' build-3/bin/ostestr
cp -p os_testr/subunit_trace.py build-3/bin/subunit-trace
%{__sed} -i -e '1s,/usr/bin/env python,%{__python3},' build-3/bin/subunit-trace
PATH=$(pwd)/build-3/bin:$PATH \
PYTHONPATH=$(pwd) \
%{__python3} os_testr/ostestr.py
%endif
%endif

%if %{with doc}
sphinx-build-2 -b html doc/source doc/build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%{__rm} -r $RPM_BUILD_ROOT%{py_sitescriptdir}/os_testr/tests

for f in generate-subunit ostestr subunit-trace subunit2html ; do
	%{__mv} $RPM_BUILD_ROOT%{_bindir}/$f $RPM_BUILD_ROOT%{_bindir}/${f}-2
done
%endif

%if %{with python3}
%py3_install

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/os_testr/tests

for f in generate-subunit ostestr subunit-trace subunit2html ; do
	%{__mv} $RPM_BUILD_ROOT%{_bindir}/$f $RPM_BUILD_ROOT%{_bindir}/${f}-3
	ln -sf $f-3 $RPM_BUILD_ROOT%{_bindir}/${f}
done
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README.rst
%attr(755,root,root) %{_bindir}/generate-subunit-2
%attr(755,root,root) %{_bindir}/ostestr-2
%attr(755,root,root) %{_bindir}/subunit-trace-2
%attr(755,root,root) %{_bindir}/subunit2html-2
%{py_sitescriptdir}/os_testr
%{py_sitescriptdir}/os_testr-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-os-testr
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README.rst
%attr(755,root,root) %{_bindir}/generate-subunit
%attr(755,root,root) %{_bindir}/generate-subunit-3
%attr(755,root,root) %{_bindir}/ostestr
%attr(755,root,root) %{_bindir}/ostestr-3
%attr(755,root,root) %{_bindir}/subunit-trace
%attr(755,root,root) %{_bindir}/subunit-trace-3
%attr(755,root,root) %{_bindir}/subunit2html
%attr(755,root,root) %{_bindir}/subunit2html-3
%{py3_sitescriptdir}/os_testr
%{py3_sitescriptdir}/os_testr-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc doc/build/html/{_static,contributor,install,user,*.html,*.js}
%endif
