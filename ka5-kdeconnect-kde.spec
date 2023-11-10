#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	23.08.3
%define		kframever	5.101.0
%define		qtver		5.15.2
%define		kaname		kdeconnect-kde
Summary:	KDE Connect - desktop app
Name:		ka5-%{kaname}
Version:	23.08.3
Release:	1
License:	BSD 3 Clause/GPL v2/GPL v3
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	5e29b775b0879589954cfab3f71a01b2
URL:		http://www.kde.org/
BuildRequires:	Qt5Core-devel >= 5.15.2
BuildRequires:	Qt5DBus-devel >= 5.15.2
BuildRequires:	Qt5Gui-devel >= 5.15.2
BuildRequires:	Qt5Multimedia-devel
BuildRequires:	Qt5Network-devel >= 5.15.2
BuildRequires:	Qt5Qml-devel >= 5.15.11
BuildRequires:	Qt5Quick-controls2-devel
BuildRequires:	Qt5Quick-devel
BuildRequires:	Qt5Test-devel
BuildRequires:	Qt5WaylandClient-devel
BuildRequires:	Qt5X11Extras-devel
BuildRequires:	cmake >= 3.20
BuildRequires:	fontconfig-devel
BuildRequires:	freetype-devel
BuildRequires:	gettext-devel
BuildRequires:	gettext-devel
BuildRequires:	kf5-extra-cmake-modules >= 5.93.0
BuildRequires:	kf5-kauth-devel >= 5.93.0
BuildRequires:	kf5-kcmutils-devel >= 5.101.0
BuildRequires:	kf5-kconfigwidgets-devel >= 5.110.0
BuildRequires:	kf5-kcoreaddons-devel >= 5.109.0
BuildRequires:	kf5-kdbusaddons-devel >= 5.101.0
BuildRequires:	kf5-kdoctools-devel >= 5.101.0
BuildRequires:	kf5-kguiaddons-devel >= 5.101.0
BuildRequires:	kf5-ki18n-devel >= 5.101.0
BuildRequires:	kf5-kiconthemes-devel >= 5.101.0
BuildRequires:	kf5-kio-devel >= 5.101.0
BuildRequires:	kf5-kirigami2-devel >= 5.101.0
BuildRequires:	kf5-knotifications-devel >= 5.101.0
BuildRequires:	kf5-kpackage-devel
BuildRequires:	kf5-kpeople-devel >= 5.101.0
BuildRequires:	kf5-kservice-devel >= 5.101.0
BuildRequires:	kf5-kwidgetsaddons-devel >= %{kframever}
BuildRequires:	kf5-kwindowsystem-devel >= 5.101.0
BuildRequires:	kf5-modemmanager-qt-devel >= 5.101.0
BuildRequires:	kf5-plasma-wayland-protocols-devel
BuildRequires:	kf5-qqc2-desktop-style-devel >= 5.101.0
BuildRequires:	kf5-solid-devel >= 5.101.0
BuildRequires:	ninja
BuildRequires:	qca-qt5-devel >= 2.1.0
BuildRequires:	qt5-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	shared-mime-info
BuildRequires:	tar >= 1:1.22
BuildRequires:	wayland-protocols >= 1.9
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
KDE Connect is a multi-platform app that allows your devices to
communicate (eg: your phone and your computer).

(Some) Features
- **Shared clipboard**: copy and paste between your phone and your
  computer (or any other device).
- **Notification sync**: Read and reply to your Android notifications
  from the desktop.
- **Share files and URLs** instantly from one device to another
  including some filesystem integration.
- **Multimedia remote control**: Use your phone as a remote for Linux
  media players.
- **Virtual touchpad**: Use your phone screen as your computer's
  touchpad and keyboard.
- **Presentation remote**: Advance your presentation slides straight
  from your phone.
- **Run Commands**: Run shell commands on your computer from your
  phone.
- **Access SMS**: Read, send and reply to SMS and MMS from your
  computer.

All this is done completely wirelessly, utilising TLS encryption.

%prep
%setup -q -n %{kaname}-%{version}

%build
%cmake \
	-B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DHTML_INSTALL_DIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON
%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

# not supported by glibc yet
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/ie
%find_lang %{kaname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{kaname}.lang
%defattr(644,root,root,755)
/etc/xdg/autostart/org.kde.kdeconnect.daemon.desktop
%attr(755,root,root) %{_bindir}/kdeconnect-app
%attr(755,root,root) %{_bindir}/kdeconnect-cli
%attr(755,root,root) %{_bindir}/kdeconnect-handler
%attr(755,root,root) %{_bindir}/kdeconnect-indicator
%attr(755,root,root) %{_bindir}/kdeconnect-settings
%attr(755,root,root) %{_bindir}/kdeconnect-sms
%ghost %{_libdir}/libkdeconnectcore.so.??
%attr(755,root,root) %{_libdir}/libkdeconnectcore.so.*.*.*
%ghost %{_libdir}/libkdeconnectinterfaces.so.??
%attr(755,root,root) %{_libdir}/libkdeconnectinterfaces.so.*.*.*
%ghost %{_libdir}/libkdeconnectpluginkcm.so.??
%attr(755,root,root) %{_libdir}/libkdeconnectpluginkcm.so.*.*.*
%dir %{_libdir}/qt5/plugins/kdeconnect
%dir %{_libdir}/qt5/plugins/kdeconnect/kcms
%attr(755,root,root) %{_libdir}/qt5/plugins/kdeconnect/kcms/kdeconnect_clipboard_config.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kdeconnect/kcms/kdeconnect_runcommand_config.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kdeconnect/kcms/kdeconnect_sendnotifications_config.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kdeconnect/kcms/kdeconnect_share_config.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kdeconnect/kdeconnect_battery.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kdeconnect/kdeconnect_bigscreen.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kdeconnect/kdeconnect_clipboard.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kdeconnect/kdeconnect_connectivity_report.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kdeconnect/kdeconnect_contacts.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kdeconnect/kdeconnect_findmyphone.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kdeconnect/kdeconnect_lockdevice.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kdeconnect/kdeconnect_mmtelephony.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kdeconnect/kdeconnect_mousepad.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kdeconnect/kdeconnect_mpriscontrol.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kdeconnect/kdeconnect_mprisremote.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kdeconnect/kdeconnect_notifications.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kdeconnect/kdeconnect_photo.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kdeconnect/kdeconnect_ping.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kdeconnect/kdeconnect_presenter.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kdeconnect/kdeconnect_remotecommands.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kdeconnect/kdeconnect_remotecontrol.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kdeconnect/kdeconnect_remotekeyboard.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kdeconnect/kdeconnect_remotesystemvolume.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kdeconnect/kdeconnect_runcommand.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kdeconnect/kdeconnect_screensaver_inhibit.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kdeconnect/kdeconnect_sendnotifications.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kdeconnect/kdeconnect_sftp.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kdeconnect/kdeconnect_share.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kdeconnect/kdeconnect_sms.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kdeconnect/kdeconnect_telephony.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kdeconnect/kdeconnect_virtualmonitor.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kf5/kfileitemaction/kdeconnectfileitemaction.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kf5/kio/kdeconnect.so
%attr(755,root,root) %{_libdir}/qt5/plugins/plasma/kcms/systemsettings_qwidgets/kcm_kdeconnect.so
%dir %{_libdir}/qt5/qml/org/kde/kdeconnect
%{_libdir}/qt5/qml/org/kde/kdeconnect/DBusProperty.qml
%{_libdir}/qt5/qml/org/kde/kdeconnect/PluginChecker.qml
%{_libdir}/qt5/qml/org/kde/kdeconnect/RemoteKeyboard.qml
%attr(755,root,root) %{_libdir}/qt5/qml/org/kde/kdeconnect/libkdeconnectdeclarativeplugin.so
%{_libdir}/qt5/qml/org/kde/kdeconnect/qmldir
%attr(755,root,root) %{_prefix}/libexec/kdeconnectd
%{_datadir}/Thunar/sendto/kdeconnect-thunar.desktop
%{_desktopdir}/kcm_kdeconnect.desktop
%{_desktopdir}/org.kde.kdeconnect-settings.desktop
%{_desktopdir}/org.kde.kdeconnect.app.desktop
%{_desktopdir}/org.kde.kdeconnect.daemon.desktop
%{_desktopdir}/org.kde.kdeconnect.handler.desktop
%{_desktopdir}/org.kde.kdeconnect.nonplasma.desktop
%{_desktopdir}/org.kde.kdeconnect.sms.desktop
%dir %{_datadir}/contractor
%{_datadir}/contractor/kdeconnect.contract
%{_datadir}/dbus-1/services/org.kde.kdeconnect.service
%dir %{_datadir}/deepin
%dir %{_datadir}/deepin/dde-file-manager
%dir %{_datadir}/deepin/dde-file-manager/oem-menuextensions
%{_datadir}/deepin/dde-file-manager/oem-menuextensions/kdeconnect-dde.desktop
%{_iconsdir}/hicolor/16x16/status/laptopconnected.svg
%{_iconsdir}/hicolor/16x16/status/laptopdisconnected.svg
%{_iconsdir}/hicolor/16x16/status/laptoptrusted.svg
%{_iconsdir}/hicolor/16x16/status/smartphoneconnected.svg
%{_iconsdir}/hicolor/16x16/status/smartphonedisconnected.svg
%{_iconsdir}/hicolor/16x16/status/smartphonetrusted.svg
%{_iconsdir}/hicolor/16x16/status/tabletconnected.svg
%{_iconsdir}/hicolor/16x16/status/tabletdisconnected.svg
%{_iconsdir}/hicolor/16x16/status/tablettrusted.svg
%{_iconsdir}/hicolor/16x16/status/tvconnected.svg
%{_iconsdir}/hicolor/16x16/status/tvdisconnected.svg
%{_iconsdir}/hicolor/16x16/status/tvtrusted.svg
%{_iconsdir}/hicolor/22x22/status/laptopconnected.svg
%{_iconsdir}/hicolor/22x22/status/laptopdisconnected.svg
%{_iconsdir}/hicolor/22x22/status/laptoptrusted.svg
%{_iconsdir}/hicolor/22x22/status/smartphoneconnected.svg
%{_iconsdir}/hicolor/22x22/status/smartphonedisconnected.svg
%{_iconsdir}/hicolor/22x22/status/smartphonetrusted.svg
%{_iconsdir}/hicolor/22x22/status/tabletconnected.svg
%{_iconsdir}/hicolor/22x22/status/tabletdisconnected.svg
%{_iconsdir}/hicolor/22x22/status/tablettrusted.svg
%{_iconsdir}/hicolor/22x22/status/tvconnected.svg
%{_iconsdir}/hicolor/22x22/status/tvdisconnected.svg
%{_iconsdir}/hicolor/22x22/status/tvtrusted.svg
%{_iconsdir}/hicolor/32x32/status/laptopconnected.svg
%{_iconsdir}/hicolor/32x32/status/laptopdisconnected.svg
%{_iconsdir}/hicolor/32x32/status/laptoptrusted.svg
%{_iconsdir}/hicolor/32x32/status/smartphoneconnected.svg
%{_iconsdir}/hicolor/32x32/status/smartphonedisconnected.svg
%{_iconsdir}/hicolor/32x32/status/smartphonetrusted.svg
%{_iconsdir}/hicolor/32x32/status/tabletconnected.svg
%{_iconsdir}/hicolor/32x32/status/tabletdisconnected.svg
%{_iconsdir}/hicolor/32x32/status/tablettrusted.svg
%{_iconsdir}/hicolor/32x32/status/tvconnected.svg
%{_iconsdir}/hicolor/32x32/status/tvdisconnected.svg
%{_iconsdir}/hicolor/32x32/status/tvtrusted.svg
%{_iconsdir}/hicolor/scalable/apps/kdeconnect.svg
%{_iconsdir}/hicolor/scalable/apps/kdeconnectindicator.svg
%{_iconsdir}/hicolor/scalable/apps/kdeconnectindicatordark.svg
%dir %{_datadir}/kdeconnect
%{_datadir}/kdeconnect/kdeconnect_clipboard_config.qml
%{_datadir}/kdeconnect/kdeconnect_runcommand_config.qml
%{_datadir}/kdeconnect/kdeconnect_sendnotifications_config.qml
%{_datadir}/kdeconnect/kdeconnect_share_config.qml
%{_datadir}/knotifications5/kdeconnect.notifyrc
%{_datadir}/kservices5/plasma-kdeconnect.desktop
%{_datadir}/metainfo/org.kde.kdeconnect.appdata.xml
%{_datadir}/metainfo/org.kde.kdeconnect.metainfo.xml
%{_datadir}/nautilus-python/extensions/kdeconnect-share.py
%dir %{_datadir}/plasma/plasmoids/org.kde.kdeconnect
%dir %{_datadir}/plasma/plasmoids/org.kde.kdeconnect/contents
%dir %{_datadir}/plasma/plasmoids/org.kde.kdeconnect/contents/ui
%{_datadir}/plasma/plasmoids/org.kde.kdeconnect/contents/ui/Battery.qml
%{_datadir}/plasma/plasmoids/org.kde.kdeconnect/contents/ui/Clipboard.qml
%{_datadir}/plasma/plasmoids/org.kde.kdeconnect/contents/ui/CompactRepresentation.qml
%{_datadir}/plasma/plasmoids/org.kde.kdeconnect/contents/ui/Connectivity.qml
%{_datadir}/plasma/plasmoids/org.kde.kdeconnect/contents/ui/DeviceDelegate.qml
%{_datadir}/plasma/plasmoids/org.kde.kdeconnect/contents/ui/FindMyPhone.qml
%{_datadir}/plasma/plasmoids/org.kde.kdeconnect/contents/ui/FullRepresentation.qml
%{_datadir}/plasma/plasmoids/org.kde.kdeconnect/contents/ui/Photo.qml
%{_datadir}/plasma/plasmoids/org.kde.kdeconnect/contents/ui/RemoteCommands.qml
%{_datadir}/plasma/plasmoids/org.kde.kdeconnect/contents/ui/SMS.qml
%{_datadir}/plasma/plasmoids/org.kde.kdeconnect/contents/ui/Sftp.qml
%{_datadir}/plasma/plasmoids/org.kde.kdeconnect/contents/ui/Share.qml
%{_datadir}/plasma/plasmoids/org.kde.kdeconnect/contents/ui/VirtualMonitor.qml
%{_datadir}/plasma/plasmoids/org.kde.kdeconnect/contents/ui/main.qml
%{_datadir}/plasma/plasmoids/org.kde.kdeconnect/metadata.desktop
%{_datadir}/plasma/plasmoids/org.kde.kdeconnect/metadata.json
%{_datadir}/qlogging-categories5/kdeconnect-kde.categories
%{zsh_compdir}/_kdeconnect
