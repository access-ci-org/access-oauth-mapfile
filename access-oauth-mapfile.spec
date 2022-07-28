###############################################################################
# Spec file for access-oauth-mapfile
################################################################################
################################################################################
#
#Macros to use in specfile
%define version %{getenv:VER}
%define release %{getenv:REL}
Summary: Utility scripts for generating an XSEDE OAuth mapfile
Name: access-oauth-mapfile
Version: %version
Release: %release
License: GPL
URL: http://access-ci.org
%undefine _disable_source_fetch
Source0: https://software.xsede.org/development/access-oauth-mapfile/access-oauth-mapfile-%version-%release/access-oauth-mapfile-%version-%release.tgz
Group: System
Packager: XSEDE, Galen Arnold, Eric Blau, JP Navarro
Requires: bash
Requires: python3
#BuildRoot: ~/eclipse-workspace/xci-196/rpmbuild/

# Build with the following syntax:
# rpmbuild --target noarch -bb access-oauth-mapfile.spec

%description
A collection of utility scripts for generating an access user map file 
mapping oauth identities to local user accounts.

%prep
################################################################################
# Create the build tree and copy the files from the development directories    #
# into the build tree.                                                         #
################################################################################
echo "BUILDROOT = $RPM_BUILD_ROOT"
#%setup -n $RPM_BUILD_ROOT/usr/local/share/utils/access_oauth_mapfile
%setup -c access_oauth_mapfile-%version-%release

%install
# create target dirs
#install -p -d -m 0755 usr/local/share/utils/access_oauth_mapfile

# copy files
mkdir -p $RPM_BUILD_ROOT/usr/local/share/utils/access_oauth_mapfile
cp -a * $RPM_BUILD_ROOT/usr/local/share/utils/access_oauth_mapfile

#exit

%files
%attr(0744, root, root) /usr/local/share/utils/access_oauth_mapfile/*
%attr(0755, root, root) /usr/local/share/utils/access_oauth_mapfile/docs/
%attr(0744, root, root) /usr/local/share/utils/access_oauth_mapfile/docs/*
%attr(0755, root, root) /usr/local/share/utils/access_oauth_mapfile/bin/
%attr(0755, root, root) /usr/local/share/utils/access_oauth_mapfile/bin/*
%attr(0755, root, root) /usr/local/share/utils/access_oauth_mapfile/etc/
%attr(0600, root, root) /usr/local/share/utils/access_oauth_mapfile/etc/*.json
%attr(0744, root, root) /usr/local/share/utils/access_oauth_mapfile/etc/gcs-mapfile-lookup.json

%pre
mkdir -p /etc/grid-security

%post
################################################################################
# Set up cron script
################################################################################
cd /etc
# If not there already, Add link to create_motd to cron.daily
cd /etc/cron.hourly
if [ ! -L access-oauth-mapfile.sh ]
then
   ln -s /usr/local/share/utils/access_oauth_mapfile/bin/access-oauth-mapfile.sh
fi

# create the initial oauth map file
#/usr/local/share/utils/access_oauth_mapfile/bin/access-oauth-mapfile.sh

%postun
# remove installed files and links
rm /etc/cron.hourly/access-oauth-mapfile.sh

%clean
rm -rf $RPM_BUILD_ROOT/usr/local/share/utils/access_oauth_mapfile

%changelog
* Thu Jul 28 2022 Eric Blau <blau@anl.gov>
  - change references to XSEDE to ACCESS and add support for the transition from XSEDE services to ACCESS services
* Fri Apr 9 2021 Eric Blau <blau@anl.gov>
  - cleaned up naming convention to xsede-oauth-mapfile
* Wed Jan 13 2021 Eric Blau <blau@anl.gov>
  - reconstructed revisions for 1.0.2+
* Wed Jul 17 2019 Galen Arnold <gwarnold@illinois.edu>
  - The original package includes useful scripts to generate the oauth
    map file.
