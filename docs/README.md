***
# Installing the xsede-oauth-mapfile tool
***

This package generates a file called **xsede-oauth-mapfile** containing entries like:

    {xsede_username}@xsede.org {local_username}

Each entry maps an XSEDE OAuth identity of the form {xsede_username}@xsede.org
to the corresponding local username on a specific XSEDE resource. An XSEDE OAuth
identity may have multiple lines mapping it to different local usernames. The mapping
information comes from the XSEDE Central Database (XCDB) and is accessed by this
software through an API.

XSEDE's Globus Connect Server (GCS) v5.4+ and other tools use these mappings to
access local resources as the authenticated user.

## Install

Choose either RPM or TAR install.

#### RPM Install

Setup XSEDE RPM repository trust:

  * For production software use [Production Repo Trust Instructions](https://software.xsede.org/production/repo/repoconfig.txt)
  * For development/testing software use [Development Repo Trust Instructions](https://software.xsede.org/development/repo/repoconfig.txt)

Install package:

     $ yum install xsede-oauth-mapfile

The RPM installs files under /usr/local/share/utils/xsede_oauth_mapfile/ by default,
except as noted below. The default location for the generated mapfile is:

    /etc/grid-security/xsede-oauth-mapfile

#### TAR Install

Download the latest Production or Development/Testing tar from either:
* https://software.xsede.org/production/xsede-oauth-mapfile/latest
* https://software.xsede.org/development/xsede-oauth-mapfile/latest

Execute:

    $ mkdir {arbitrary_path}/xsede-oauth-mapfile-<version>
    $ cd {arbitrary_path}/xsede-oauth-mapfile-<version>
    $ tar -xzf {downloaded_file}

## Request API Access Key

If you don't have an XDCDB access API-KEY from a previous xsede-oauth-mapfile install,
request one by following the instructions at https://xsede-xdcdb-api.xsede.org/ by Clicking
on the "Generate APIKEY" link and following the displayed instructions. In the e-mail to
help@xsede.org specify <AGENT> "spacct". If you are accessing the API for an XSEDE
allocated resource, provide the official XDCDB Resource Name, like "expanse.sdsc.xsede.org".
If you are testing the xsede-oauth-mapfile tool, or accessing mapping information for some
other reason, provide the fully qualified hostname that will access the API as the XDCDB Resource
Name. The XDCDB Resource Name in the request will not limit which resources can be looked
up with API calls. XSEDE's active XDCDB Resource Names are listed at:
* https://info.xsede.org/wh1/warehouse-views/v1/resources-xdcdb-active/?format=html

The e-mail request will register your xsede-oauth-mapfile deployment in XDCDB and provide
you an API-KEY for the xsede-oauth-mapfile tool to use to access the XDCDB API.

### Configure xsede-oauth-mapfile

If you have an etc/xsede-oauth-mapfile-config.json from a previous install, copy it to
this install etc/ directory, otherwise create it by copying the newly RPM/TAR installed
etc/xsede-oauth-mapfile-config-template.json.

Edit etc/xsede-oauth-mapfile-config.json and set:

    "XA-AGENT": "spacct",
    "XA-RESOURCE": "<XDCDB resource name>",
    "XA-API-KEY": "<your API-KEY>"

The API-KEY may be from a previous xsede-oauth-mapfile configuration or a new one
in the previous step.

Set the permissions for the config for read-only by root to keep the API-KEY private:

    $ chmod 0600 etc/xsede-oauth-mapfile-config.json

In bin/xsede-oauth-mapfile.sh:
 * Set MAP_FILE to where you want your production mapfile
 * Set MAP_FILE_BASE to your base xsede-oauth-mapfile installation directory

If you have additional local mappings that don't come from XDCDB, place them in
/etc/grid-security/xsede-oauth-mapfile.local, or customize the LOCAL_FILE variable
in bin/xsede-oauth-mapfile.sh to point to your local mappings.

XDCDB generated mappings and local mappings will be combined into the MAP_FILE.

### Setup to generate using cron

Execute as root:

    $ cd /etc/cron.hourly
    $ ln -s /usr/local/share/utils/xsede_oauth_mapfile/bin/xsede_oauth_mapfile.sh

### Obtaining Support

Report xsede-oauth-mapfile bugs, questions, and suggestions to help@xsede.org.

## NOTES

**bin/xsede-oauth-mapfile.py** - Python map file generator.
It should run with default python3 and included modules.

**bin/gcs-mapfile-lookup** - Script used by GCS v5.4 to lookup values in
the **xsede-oauth-mapfile**. Instructions for doing so are in the GCS v5.4 Installation Guide.
