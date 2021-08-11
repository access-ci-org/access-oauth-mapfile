#!/bin/bash

# The real map_file used by services
MAP_FILE=/etc/grid-security/xsede-oauth-mapfile
# The config file used by this invokation of the xsede-oauth-mapfile script
CONFIG_FILE=etc/xsede-oauth-mapfile-config.json
# The mapfile generated from XDCDB in the current working directory
GEN_FILE=xsede-oauth-mapfile
# The base install directory where mapfile generation is run from
MAP_FILE_BASE=/usr/local/share/utils/xsede_oauth_mapfile
# Other locally managed mapfile entries
LOCAL_FILE=/etc/grid-security/xsede-oauth-mapfile.local
# The lockfile
#MAP_LOCK=./GEN_MAP.LOCK
MAP_LOCK=./${GEN_FILE}.LOCK
echo $MAP_LOCK

if [ -d $MAP_FILE_BASE ]
then
	cd $MAP_FILE_BASE
else
	# go ahead and linux throw the error
	cd $MAP_FILE_BASE
	exit $?
fi
cd $MAP_FILE_BASE
if [ -f $MAP_LOCK ]
then
	echo "A map_file generations process is running... exiting"
	exit 1
fi

# Do the update work
touch $MAP_LOCK
./bin/xsede-oauth-mapfile.py -m $GEN_FILE -c $CONFIG_FILE

# If you have local mappings place them in $LOCAL_FILE
# Append local mappings to the generated file
if [ -f $LOCAL_FILE ]
then
    cat $LOCAL_FILE >>$GEN_FILE
fi

cp -p $GEN_FILE $MAP_FILE

rm $MAP_LOCK
