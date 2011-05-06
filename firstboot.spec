%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Summary: Initial system configuration utility
Name: firstboot
URL: http://fedoraproject.org/wiki/FirstBoot
Version: 1.119
Release: 1%{?dist}.1.R
# This is a Red Hat maintained package which is specific to
# our distribution.  Thus the source is only available from
# within this srpm.
Source0: %{name}-%{version}.tar.bz2

License: GPLv2+
Group: System Environment/Base
ExclusiveOS: Linux
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: gettext
BuildRequires: python-devel, python-setuptools-devel
Requires: pygtk2, python
Requires: setuptool, libuser-python, system-config-users, system-config-date
Requires: authconfig-gtk, python-meh
Requires: system-config-keyboard
Requires: python-ethtool
Requires: cracklib-python
Requires: systemd-units
Requires: firstboot(windowmanager)
Requires(post): chkconfig

%define debug_package %{nil}

Obsoletes: firstboot-tui < 1.90-1

Patch10: firstboot-1.117-rfremix-15.patch
Patch11: firstboot-1.117-rfr-sudo.patch

%description
The firstboot utility runs after installation.  It guides the user through
a series of steps that allows for easier configuration of the machine.

%prep
%setup -q
%patch10 -p1 -b .rfremix-15
%patch11 -p1 -b .rfr-sudo

%build

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} SITELIB=%{python_sitelib} install
rm %{buildroot}/%{_datadir}/firstboot/modules/additional_cds.py*
%find_lang %{name}

%clean
rm -rf %{buildroot}

%post
if [ $1 -ne 2 -a ! -f /etc/sysconfig/firstboot ]; then
  systemctl enable firstboot-text.service >/dev/null 2>&1 || :
  systemctl enable firstboot-graphical.service >/dev/null 2>&1 || :
fi

%preun
if [ $1 = 0 ]; then
  rm -rf /usr/share/firstboot/*.pyc
  rm -rf /usr/share/firstboot/modules/*.pyc
  systemctl disable firstboot-graphical.service >/dev/null 2>&1 || :
  systemctl disable firstboot-text.service >/dev/null 2>&1 || :
fi

%files -f %{name}.lang
%defattr(-,root,root,-)
%dir %{_datadir}/firstboot/
%dir %{_datadir}/firstboot/modules/
%dir %{_datadir}/firstboot/themes/
%dir %{_datadir}/firstboot/themes/default
%config %{_initrddir}/firstboot
%{python_sitelib}/*
%{_sbindir}/firstboot
%{_datadir}/firstboot/modules/create_user.py*
%{_datadir}/firstboot/modules/date.py*
%{_datadir}/firstboot/modules/eula.py*
%{_datadir}/firstboot/modules/rfremix.py*
%{_datadir}/firstboot/modules/welcome.py*
%{_datadir}/firstboot/themes/default/*
/lib/systemd/system/firstboot-text.service
/lib/systemd/system/firstboot-graphical.service

%changelog
* Fri May  6 2011 Arkady L. Shane <ashejn@yandex-team.ru> 1.119-1.1.R
- upfate to 1.119

* Wed May  4 2011 Arkady L. Shane <ashejn@yandex-team.ru> 1.118-1.1.R
- update to 1.118

* Sat Apr 16 2011 Arkady L. Shane <ashejn@yandex-team.ru> 1.117-2.4.R
- use schemas instead gconf where it needed

* Sat Apr 16 2011 Arkady L. Shane <ashejn@yandex-team.ru> 1.117-2.3.R
- drop legacy gconf rules
- drop comments
- apply gconf rule only if application is present

* Wed Mar 23 2011 Arkady L. Shane <ashejn@yandex-team.ru> 1.117-2.2
- added sudo patch

* Sat Mar 19 2011 Arkady L. Shane <ashejn@yandex-team.ru> 1.117-2.1
- RFRemixify
- added new Eula
- added rfremix config screens

* Fri Feb 25 2011 Brian C. Lane <bcl@redhat.com> 1.117-2
- We need to quit plymouth before running firstboot (#679171)

* Fri Feb 18 2011 Martin Gracik <mgracik@redhat.com> 1.117-1
- Fix username guessing with unicode chars (#678070)

* Tue Feb 15 2011 Martin Gracik <mgracik@redhat.com> 1.116-1
- systemd's ValidNoProcess renamed to RemainAfterExit
- Don't run Xorg with -nr option and use vt1
- Translation updates

* Fri Jan 14 2011 Martin Gracik <mgracik@redhat.com> 1.115-1
- Don't enable firstboot service on upgrade (#626676)
- Set HOME to /root rather than / (#578903)
- Translation updates

* Mon Dec 20 2010 Martin Gracik <mgracik@redhat.com> 1.114-1
- Support other window managers than metacity (#605675)
- firstboot -> metacity dep (#605675) (rdieter)
- Change how we check for user account
- Use StrengthMeter widget instead of ProgressBar
- Add StrengthMeter widget to pwcheck
- Increase the weight of cracklib password check
- Show the password strength in a progress bar
- Add strength fraction property to pwcheck
- Translation updates
- Change the way we warn for a weak password
- Add the pwcheck module for getting the password strength
- Do not show tabs in date and time module
- Allow the user to be added to wheel group (#462161)
- Guess user name from full name (#517269)

* Thu Aug 26 2010 Martin Gracik <mgracik@redhat.com> 1.113-1
- Updated the .pot file
- Changed string formatting for translations (#618610)
- Syntax changed in new systemd
- Make sure we start before tty1 in text mode
- Don't use the legacy sysv services anymore
- Translation updates

* Tue Aug 10 2010 Martin Gracik <mgracik@redhat.com> 1.112-1
- Add systemd support (adamw)
- Translation updates

* Thu Jul 15 2010 Martin Gracik <mgracik@redhat.com> 1.111-1
- Fixed indenting
- Set the LANG variable if running our own X frontend (#599296)
- Added the spec file obsoletes version number
- Add requirement for cracklib-python
- Allow more control when creating new user (#602030)
- Fix functioning of module sets (#595320)
- Don't try to use the X frontend when run in console (#537717)
- Update to work with new python-meh with report support (#562659)
- Add weak password checking (#612362)
- Source the lang.sh file instead of just i18n (#563547)
- Run Xorg with -nr option, so we have less flicker (ajax)
- Many translation updates

* Wed Oct 14 2009 Chris Lumens <clumens@redhat.com> 1.110-1
- Always attempt to display the Fedora logo, if present (jmccann).
- Fix a bunch of small firstboot UI problems (jmccann).

* Thu Sep 10 2009 Chris Lumens <clumens@redhat.com> 1.109-1
- Change the init script return value for LSB purposes (atodorov, #521828).
- We don't really need an X log file anymore (#521387).
- Pull in updated translations.
- Improve logging when modules cannot be loaded (jlaska).

* Tue Aug 11 2009 Chris Lumens <clumens@redhat.com> 1.108-1
- Move python-meh initialization to after we have gtk imported (#515419).
- Do @VERSION@ substitution on progs/firstboot.
- Switch to using system-config-keyboard for the keyboard bits (katzj).
- Stop using rhpl.ethtool (katzj).

* Tue Jul 28 2009 Chris Lumens <clumens@redhat.com> 1.107-1
- Convert to using python-meh.

* Tue May 05 2009 Chris Lumens <clumens@redhat.com> 1.106-1
- Display an error message when the user doesn't supply a password (#480927).
- Lots of translation updates.

* Fri Jan 16 2009 Chris Lumens <clumens@redhat.com> 1.105-1
- Fix a typo in starting up X.

* Tue Dec 16 2008 Chris Lumens <clumens@redhat.com> 1.104-1
- Let X tell us when it's ready to run (ajax).
- Add a Requires: for authconfig-gtk (#474733).
- Log errors changing file permissions and notify (#473191).
- Improve the dialogs around reusing a home directory (#470461).
- Fix a crash when cancelling contacting an NTP server (#475304).
- Since you have to create a user now, change the message.

* Tue Nov 04 2008 Chris Lumens <clumens@redhat.com> 1.103-1
- Try another way of waiting for X to terminate (#469501).

* Mon Oct 27 2008 Chris Lumens <clumens@redhat.com> 1.102-1
- Be smarter about finding a graphics theme to use.

* Wed Oct 22 2008 Chris Lumens <clumens@redhat.com> 1.101-1
- Wait to make sure X is completely dead before continuing (ajax).
- Don't display that ugly root weave background anymore (ajax).
- Lots of translation updates.

* Fri Sep 12 2008 Chris Lumens <clumens@redhat.com> 1.100-1
- Force creating a user unless the network button was checked (jmccann, #461656).
- Don't sit at the bootup splash screen indefinitely (#458553).

* Thu Jul 31 2008 Chris Lumens <clumens@redhat.com> 1.99-1
- Enable the correct keyboard layout (#453228).
- Remove the timezone tab from the default date & time module (#442394).
- Raise NotImplementedError instead of TypeError.
- Allow modules to focus a UI element before they are displayed (#457422).
- Lots of updated translations.

* Tue May 13 2008 Chris Lumens <clumens@redhat.com> 1.98-1
- Remove the rhgb interface.
- Use subprocess for starting X instead of rhpxl.
- Don't run system-config-display from the init if there's no X config
  file.
- Fix tracebacks when trying to chown broken symlinks (#445092).
- Set up the keyboard if firstboot is run as a program (#445281).
- Lots of updated translations.

* Wed Apr 16 2008 Chris Lumens <clumens@redhat.com> 1.97-1
- Don't allow creating a user with no password (#442613).
- In low resolution cases, wrap the sidebar text earlier (#442394).
- Update translation files for EULA URL change (stickster@gmail.com).

* Thu Apr 10 2008 Chris Lumens <clumens@redhat.com> 1.96-1
- Don't package additional_cds module for now (#441749).
- Add the date and time module (#441504).
- The license agreement has moved URLs.

* Mon Apr 07 2008 Chris Lumens <clumens@redhat.com> 1.95-4
- Fix another init script typo (#441016).

* Fri Apr 04 2008 Chris Lumens <clumens@redhat.com> 1.95-3
- Fix a typo in the init script.

* Thu Apr 03 2008 Chris Lumens <clumens@redhat.com> 1.95-2
- Require another program we need.

* Thu Apr 03 2008 Chris Lumens <clumens@redhat.com> 1.95-1
- Check for RUN_FIRSTBOOT=NO in the init script.
- Don't display broken images if files aren't found in the primary location.

* Wed Apr 02 2008 Chris Lumens <clumens@redhat.com> 1.94-1
- Look in the right directory for Fedora artwork (#439283).
- Require libuser-python (#439307).
- Translation updates.

* Wed Mar 26 2008 Chris Lumens <clumens@redhat.com> 1.93-1
- Add in the text mode interface.
- Wait for the X server to exit (#431469).
- Lots of translation updates.

* Thu Jan 31 2008 Chris Lumens <clumens@redhat.com> 1.92-1
- Add a reworked user creation page (#429195).
- If the user's home dir already exists, offer to set ownership (#426631).

* Mon Jan 28 2008 Chris Lumens <clumens@redhat.com> 1.91-2
- Put module in /usr/lib64 on 64-bit platforms.

* Wed Jan 02 2008 Chris Lumens <clumens@redhat.com> 1.91-1
- Reorganize to provide a python module.
- Provide real help output for the firstboot program.

* Wed Dec 05 2007 Chris Lumens <clumens@redhat.com> 1.90-3
- Don't provide a debuginfo package (#413011).

* Tue Nov 20 2007 Chris Lumens <clumens@redhat.com> 1.90-2
- Obsolete the old firstboot-tui package that no longer exists.

* Mon Nov 19 2007 Chris Lumens <clumens@redhat.com> 1.90-1
- First packaging of the new firstboot program.
