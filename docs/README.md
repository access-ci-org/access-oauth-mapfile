***
# Installing the access-oauth-mapfile tool
***

This package generates a file called **access-oauth-mapfile** containing entries like:

    {access_username}@access-ci.org {local_username}

Each entry maps an ACCESS OAuth identity in the form {access_username}@access-ci.org to the
corresponding local username on a specific ACCESS resource. An ACCESS OAuth identity
may have multiple lines mapping it to multiple local usernames. These mappings come
from the ACCESS Central Database (ACDB) and are accessed by this tool through an API.

ACCESS's Globus Connect Server (GCS) v5.4+ and other tools use these mappings to
access local resources as the authenticated user.

## Install

Choose either RPM or TAR install.

#### RPM Install

Install the desired RPM release from [https://github.com/access-ci-org/access-oauth-mapfile/releases](https://github.com/access-ci-org/access-oauth-mapfile/releases).

The RPM installs files under /usr/local/share/utils/access_oauth_mapfile/ by default.

#### TAR Install

Download the desired TAR release from [https://github.com/access-ci-org/access-oauth-mapfile/releases](https://github.com/access-ci-org/access-oauth-mapfile/releases).

Execute:

    $ mkdir {arbitrary_path}/access-oauth-mapfile-<version>
    $ cd {arbitrary_path}/access-oauth-mapfile-<version>
    $ tar -xzf {downloaded_file}

Edit the untarred bin/access-oauth-mapfile.sh and set MAP_FILE_BASE to the directory that you just untarred.


## Request API Access Key

If you don't have an ACDB access API-KEY from a previous access-oauth-mapfile install,
request one by following the instructions at https://allocations-api.access-ci.org/acdb,
Clicking on the "Generate APIKEY" link, and then perform the following steps:

Open an operations request ticket at: [https://operations.access-ci.org/open-operations-request/](https://operations.access-ci.org/open-operations-request/). You will have to login first.

In the "Request Title" enter "Allocations API-KEY installation request"
In the "Description" enter:

     "Please install the following HASH for agent spacct on resource <ACCESS RESOURCE NAME>"
     <YOUR HASH>
     "on server https://allocations-api.access-ci.org/acdb/"

If you are accessing the API for an ACCESS allocated resource, provide the official ACDB Resource Name,
like "expanse.sdsc.access-ci.org". If you are are testing the access-oauth-mapfile tool, or accessing mapping
information for some other reason, provide the fully qualified hostname that will access the API as the ACDB
Resource Name. The resource name you give here will be used as the XA-RESOURCE in the access-oauth-mapfile
configuration, acting as the API Client ID and does not limit which resources mappings can be looked up with
API calls. ACCESS's active ACDB Resource Names are listed at:

* https://operations-api.access-ci.org/wh2/cider/v1/access-active/?format=html&sort=latest_status

The email request will register your access-oauth-mapfile deployment in ACDB and authorize it
to access the ACDB API using your API-KEY.

### Configure access-oauth-mapfile

If you have an etc/access-oauth-mapfile-config.json from a previous install, copy it to this install etc/ directory,
otherwise create it by copying the newly RPM/TAR installed etc/access-oauth-mapfile-config-template.json.

Edit etc/access-oauth-mapfile-config.json and set:

    "XA-AGENT": "spacct",
    "XA-RESOURCE": "<ACDB resource name> or <other fully qualified API client hostname>",
    "MAP-RESOURCE": "<ACDB resource name>",
    "XA-API-KEY": "<your API-KEY>"

Where "XA-RESOURCE" identifies the Client ID (ACDB Resource Name above) that is retrieving the mappings,
and "MAP-RESOURCE" is which ACCESS resource mappings you are retrieving. On a production resource both of
these are normally the same, but in a testing or other situation a testing server / XA-RESOURCE may be
accessing mappings for a production MAP-RESOURCE.

The API-KEY may be from a previous access-oauth-mapfile configuration or a new one from the previous step.

Set the permissions for the config for read-only by root to keep the API-KEY private:

    $ chmod 0600 etc/access-oauth-mapfile-config.json

If you have additional local mappings that don't come from ACDB, place them in
/etc/grid-security/access-oauth-mapfile.local, or customize the LOCAL_FILE variable
in bin/access-oauth-mapfile.sh to point to your local mappings.

ACDB generated mappings and local mappings will be combined into the MAP_FILE.

If you change the default path of the mapfiles from /etc/grid-security/ to another directory,
also update the "mapfile = " paths in the bin/gcs-mapfile-lookup.py script. 

### Setup to generate using cron

Execute as root:

    $ cd /etc/cron.hourly
    $ ln -s /usr/local/share/utils/access_oauth_mapfile/bin/access-oauth-mapfile.sh

### Getting Support

Report access-oauth-mapfile bugs, questions, and suggestions by opening a ticket at [https://operations.access-ci.org/open-operations-request/](https://operations.access-ci.org/open-operations-request/).

### Advanced Usage

access-oauth-mapfile can be configured to create and maintain multiple different mapfiles, including ones based on the sets of authorized users for multiple different resources.

To create both a mapfile for resource A and one for resource B on the same machine, do the following:
1. Copy /usr/local/share/utils/access-oauth-mapfile/bin/access-oauth-mapfile.sh as /etc/cron.hourly/A.sh
2. Copy /usr/local/share/utils/access-oauth-mapfile/bin/access-oauth-mapfile.sh as /etc/cron.hourly/B.sh
3. Edit /etc/cron.hourly/A.sh, setting the following values:
  * MAP_FILE=/etc/grid-security/access-oauth-mapfile-A
  * CONFIG_FILE=etc/access-oauth-mapfile-config-A.json
  * GEN_FILE=access-oauth-mapfile-A
  * LOCAL_FILE=/etc/grid-security/access-oauth-mapfile-A.local
4. Edit /etc/cron.hourly/B.sh, setting the following values:
  * MAP_FILE=/etc/grid-security/access-oauth-mapfile-B
  * CONFIG_FILE=etc/access-oauth-mapfile-config-B.json
  * GEN_FILE=access-oauth-mapfile-B
  * LOCAL_FILE=/etc/grid-security/access-oauth-mapfile-B.local
5. copy /usr/local/share/utils/access-oauth-mapfile/etc/access-oauth-mapfile-config-template to /usr/local/share/utils/access-oauth-mapfile/etc/xsed-oauth-mapfile-config-A.json
6. edit /usr/local/share/utils/access-oauth-mapfile/etc/xsed-oauth-mapfile-config-A.json, setting XA-RESOURCE and XA-API-KEY to the values used when requesting your API key.  Set MAP_RESOURCE to be the ACCESS resource you wish to map oauth identity information for your "A" resource
7. copy /usr/local/share/utils/access-oauth-mapfile/etc/access-oauth-mapfile-config-template to /usr/local/share/utils/access-oauth-mapfile/etc/xsed-oauth-mapfile-config-B.json
8. edit /usr/local/share/utils/access-oauth-mapfile/etc/xsed-oauth-mapfile-config-A.json, setting XA-RESOURCE and XA-API-KEY to the values used when requesting your API key.  Set MAP_RESOURCE to be the ACCESS resource you wish to map oauth identity information for your "B" resource
9. Define any additional mappings for your "A" resource in/etc/grid-security/access-oauth-mapfile-A.local
10. Define any additional mappings for your "B" resource in/etc/grid-security/access-oauth-mapfile-B.local
11. Your mapfile for your "A" resource will be updated hourly by cron to the file /etc/grid-security/access-oauth-mapfile-A
12. Your mapfile for your "B" resource will be updated hourly by cron to the file /etc/grid-security/access-oauth-mapfile-B

## NOTES

**bin/access-oauth-mapfile.py** - Python map file generator.  It should run with default python3 and included modules.

**bin/gcs-mapfile-lookup** - Script used by GCS v5.4 to lookup values in the **access-oauth-mapfile**.
Instructions for doing so are in the GCS v5.4 Installation Guide.