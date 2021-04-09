###############################################################################
##
## xsede-oauth-mapfile
##
###############################################################################

This package generates a file called xsede-oauth-mapfile with entries like:

<xsede_username>@xsede.org <local_username>

Each entry maps an XSEDE OAuth identity of the form <xsede_username>@xsede.org
to the corresponding local username on a specific XSEDE resource. An XSEDE OAuth
identity may have multiple lines mapping it to multiple local usernames.

XSEDE's Globus Connect Server (GCS) v5.4+ and other tools can use these mappings
to map OAuth identities to local accounts.

The mapping information comes from XDCDB and is accessed through an API.

INSTALLATION

1) Configure XSEDE RPM repository trust, if installing from RPM
   For a production version use [Production Repo Trust Instructions](https://software.xsede.org/production/repo/repoconfig.txt)
   For a development/testing version use [Development Repo Trust Instructions](https://software.xsede.org/development/repo/repoconfig.txt)

2)  Install following 2a) OR 2b)

2a) Install from RPM
   $ yum install xsede-oauth-mapfile

   By default, the rpm will install files under /usr/local/share/utils/xsede_user_mapfile/
   except as noted below.  Once configured with an API-KEY, the mapfile will default to 
   /usr/local/etc/grid-security/xsede-oauth-mapfile .

2b) Install from TAR
   # From TAR
   # Download the latest Production tar or Development/Testing tar from either:
   https://software.xsede.org/production/xsede-oauth-mapfile/latest
   https://software.xsede.org/production/xsede-oauth-mapfile/

   mkdir /my/local/path/xsede-oauth-mapfile-<version>
   cd /my/local/path/xsede-oauth-mapfile-<version>
   tar -xzf <downloaded_file>

3) If this is your first install, request an XDCDB access API-KEY
   If you don't have an XDCDB access API-KEY from a previous xsede-oauth-mapfile install
     obtain one following the instructions at https://xsede-xdcdb-api.xsede.org/
   In the request specify the "spacct" agent and the resource name that you want
      mapped acccounts for.

   This request will register your xsede-oauth-mapfile deployment in XDCDB and provide an
      API-KEY for xsede-oauth-mapfile to use to access the XDCDB API.

4) Configure xsede-oauth-mapfile
   If you have an etc/xsede-oauth-mapfile-config.json from a previous install, copy it to this
   install, otherwise create it using the xsede-oauth-mapfile-config-template.json.

   Edit etc/xsede-oauth-mapfile-config.json and set
      "XA-AGENT": "spacct",
      "XA-RESOURCE": "<XDCDB resource name>",
      "XA-API-KEY": "<your API-KEY>"

    The API-KEY may be from a previous xsede-oauth-mapfile configuration, or a new one from
    step 3) above.

    Set the permissions for the config for read-only by root because it has an API-KEY:
    access the XDCDB:
       chmod 0600 etc/xsede-oauth-mapfile-config.json

5) Setup to run in cron
   In bin/xsede-oauth-mapfile.sh:
   - Set MAP_FILE to where you want your production mapfile
   - Set MAP_FILE_BASE to your base xsede-oauth-mapfile installation directory

   cd /etc/cron.hourly
   ln -s /usr/local/share/utils/xsede_oauth_mapfile/bin/xsede_oauth_mapfile.sh

NOTES

bin/xsede-oauth-mapfile.sh
    This is the file to be run from /etc/cron.hourly to keep the map file up to date.
    "xsede-oauth-mapfile.py" and protects against multiple invocations with a file-present
      flag: ./GEN_MAP.LOCK
    If that file is present the script exits with an informational message.
    The script also does a cp of the map file in order to make the process more atomic and
    less susceptible to any scripting issues that could corrupt the operational map file.

bin/xsede-oauth-mapfile.py
    Python map file generator. It should run with default python3 and included modules.

Report problems and suggestions to help@xsede.org.
