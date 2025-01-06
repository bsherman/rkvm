%bcond_with check

Name:           rkvm
Version:        0.6.1
Release:        1%{?dist}
Summary:        Shares keyboard and mouse across multiple Linux machines

License:        MIT
URL:            https://github.com/htrefil/rkvm
Source:         https://github.com/htrefil/%{name}/archive/refs/tags/%{version}.tar.gz

ExclusiveArch:  %{rust_arches}

BuildRequires:  cargo
BuildRequires:  cargo-rpm-macros >= 24
BuildRequires:  clang
BuildRequires:  libevdev-devel
BuildRequires:  rust

%description
rkvm is a tool for sharing keyboard and mouse across multiple Linux machines. 
It is based on a client/server architecture, where server is the machine 
controlling mouse and keyboard and relays events (mouse move, key presses, etc) 
to clients.


%prep
%autosetup -n %{name}-%{version} -p1
cargo vendor --locked rkvmvendor
%cargo_prep -v rkvmvendor

%build
%cargo_build
%{cargo_license_summary}
%{cargo_license} > LICENSE.dependencies

%install
install -Dpm 0755 target/release/%{name}-certificate-gen -t %{buildroot}%{_bindir}/
install -Dpm 0755 target/release/%{name}-client -t %{buildroot}%{_bindir}/
install -Dpm 0755 target/release/%{name}-server -t %{buildroot}%{_bindir}/
install -Dpm 0644 systemd/%{name}-client.service -t %{buildroot}%{_prefix}/lib/systemd/system/
install -Dpm 0644 systemd/%{name}-server.service -t %{buildroot}%{_prefix}/lib/systemd/system/
mkdir -p %{buildroot}%{_docdir}/%{name}/examples/
install -Dpm 0644 example/client.toml %{buildroot}%{_docdir}/%{name}/examples/
install -Dpm 0644 example/server.toml %{buildroot}%{_docdir}/%{name}/examples/
mkdir -p %{buildroot}%{_sysconfdir}/%{name}/
ln -s ../..%{_docdir}/%{name}/examples/client.toml %{buildroot}%{_sysconfdir}/%{name}/example-client.toml
ln -s ../..%{_docdir}/%{name}/examples/server.toml %{buildroot}%{_sysconfdir}/%{name}/example-server.toml

%if %{with check}
%check
%cargo_test
%endif

%files
%license LICENSE
%license LICENSE.dependencies
%doc README.md
%doc switch-keys.md
%{_bindir}/%{name}-certificate-gen
%{_bindir}/%{name}-client
%{_bindir}/%{name}-server
%{_prefix}/lib/systemd/system/%{name}-client.service
%{_prefix}/lib/systemd/system/%{name}-server.service
%{_docdir}/%{name}/examples/client.toml
%{_docdir}/%{name}/examples/server.toml
%{_sysconfdir}/%{name}/example-client.toml
%{_sysconfdir}/%{name}/example-server.toml

%changelog
* Mon Jan 06 2025 Benjamin Sherman <benjamin@holyarmy.org> - 0.6.1-1
- packaged rkvm for RPM
- see rkvm releases in Github for feature changes
