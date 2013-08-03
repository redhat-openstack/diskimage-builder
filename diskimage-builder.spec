%global commit 5b37036c88b93f452c2822262b7f4d953f1495da
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:		diskimage-builder
Summary:	Image building tools for OpenStack
Version:	0.0.1
Release:	3%{?dist}
License:	ASL 2.0
Group:		System Environment/Base
URL:		https://launchpad.net/diskimage-builder
Source0:	https://github.com/stackforge/diskimage-builder/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz

BuildArch: noarch
BuildRequires: python2-devel
BuildRequires: python-setuptools

Requires: kpartx
Requires: qemu-img
Requires: busybox

%prep
%setup -q -n %{name}-%{commit}

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root=%{buildroot}

mkdir -p %{buildroot}%{_sysconfdir}/sudoers.d/
mkdir -p %{buildroot}%{_datadir}/%{name}/lib
mkdir -p %{buildroot}%{_datadir}/%{name}/elements

install -p -D -m 440 %{_builddir}/%{name}-%{commit}/sudoers.d/* %{buildroot}%{_sysconfdir}/sudoers.d/
install -p -D -m 644 %{_builddir}/%{name}-%{commit}/lib/* %{buildroot}%{_datadir}/%{name}/lib
cp -vr %{_builddir}/%{name}-%{commit}/elements/ %{buildroot}%{_datadir}/%{name}

%description
Components of TripleO that are responsible for building disk images.

%files
%doc LICENSE
%doc docs/ci.md
%{_bindir}/*
%{python_sitelib}/diskimage_builder*
%{_datadir}/%{name}/lib
%{_datadir}/%{name}/elements
%config(noreplace) %attr(-,root,root) %{_sysconfdir}/sudoers.d/img-build-sudoers

%verifyscript
if ! visudo -c -f /etc/sudoers.d/img-build-sudoers; then
  echo "Problem with img-build-sudoers file!"
fi

%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 31 2013 Jeff Peeler <jpeeler@redhat.com> 0.0.1-2
- rebased and dropped patches

* Mon Jul 29 2013 Jeff Peeler <jpeeler@redhat.com> 0.0.1-1
- initial package straight from github commit sha
