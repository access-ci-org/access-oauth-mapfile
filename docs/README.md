***
# Installing the access-oauth-mapfile tool
***

This tool generates a file called **access-oauth-mapfile** containing entries like:

    {access_username}@access-ci.org {local_username}

Each entry maps an ACCESS OAuth identity in the form {access_username}@access-ci.org to the
corresponding local username on a specific ACCESS resource. An ACCESS OAuth identity
may have multiple lines mapping it to multiple local usernames. These mappings come
from the ACCESS Central Database (ACDB) and are retrieved by this tool through an API.

ACCESS's Globus Connect Server (GCS) v5.4+ and other tools use these mappings to
access local resources as the authenticated user.


## Install

Choose either RPM or TAR install.

#### RPM Install

Install the desired RPM release from [https://github.com/access-ci-org/access-oauth-mapfile/releases](https://github.com/access-ci-org/access-oauth-mapfile/releases).

The RPM installs files by default under /usr/local/share/utils/access_oauth_mapfile/.

#### TAR Install

Download the desired TAR release from [https://github.com/access-ci-org/access-oauth-mapfile/releases](https://github.com/access-ci-org/access-oauth-mapfile/releases).

Execute:

    $ mkdir {arbitrary_path}/
    $ cd {arbitrary_path}/
    $ tar -xzf {downloaded_file}

The tar will extract into the sub-directory access-oauth-mapfile-{release}.

Edit the untarred bin/access-oauth-mapfile.sh and set MAP_FILE_BASE to the directory that you just untarred.


## Request API Access Key

If you don't have an ACDB access API-KEY from a previous access-oauth-mapfile install,
request one by following the instructions at https://allocations-api.access-ci.org/acdb,
Clicking on the "Generate APIKEY" link, and then perform the following steps:

Open an operations request ticket at: [https://operations.access-ci.org/open-operations-request/](https://operations.access-ci.org/open-operations-request/).
You will have to login first.

In the "Request Title" enter "Allocations API-KEY installation request"
In the "Description" enter:

     "Please install the following HASH for agent spacct on resource <ACCESS INFO RESOURCEID>"
     <YOUR HASH>
     "on server https://allocations-api.access-ci.org/acdb/"

If you are accessing the API for an ACCESS allocated resource, provide the official ACDB Info ResourceID,
like "expanse.sdsc.access-ci.org". If you are are testing the access-oauth-mapfile tool, or accessing mapping
information for some other reason, provide the fully qualified hostname that this tool will run on. The
Info ResourceID you provide is passed to the API in the XA-RESOURCE header and represents an API Client ID.
All clients can access mappings for all resources, and which resource you want to retrieve mappings for is
configured separately. Lookup official Info ResourceIDs here:

* https://operations-api.access-ci.org/wh2/cider/v1/access-active/?format=html&sort=latest_status

The email request will register your access-oauth-mapfile deployment in ACDB and authorize it
to access the ACDB API using your API-KEY.

### Configure access-oauth-mapfile

If you have an etc/access-oauth-mapfile-config.json from a previous install, copy it to this install etc/ directory,
otherwise create it by copying the newly RPM/TAR installed etc/access-oauth-mapfile-config-template.json.

Edit etc/access-oauth-mapfile-config.json and set:

    "XA-AGENT": "spacct",
    "XA-RESOURCE": "<ACDB Info ResourceID> or <other fully qualified hostname from above>",
    "MAP-RESOURCE": "<ACDB Info ResourceID or xsede.org equivalent>",
    "XA-API-KEY": "<your API-KEY>"

Where "XA-RESOURCE" identifies the API Client ID described above, and "MAP-RESOURCE" is which ACCESS resource you want
mappings for. For "MAP-RESOURCE" first try the ACDB Info ResourceID, which only works for a small subset of current
ACCESS resources. If that doesn't retreieve mapping, try replacing the 'access-ci.org' suffix in the ID with 'xsede.org'.
NOTE: using 'xsede.org' in the "MAP-RESOURCE" has nothing to do with whether the resources was part of XSEDE, it is
due to some technical debt with how the ACCESS database identifies resources.

Keep the API-KEY private by only allowing the owner to view it, this should be root if you installed by RPM, or the account
you insalled the TAR with:

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