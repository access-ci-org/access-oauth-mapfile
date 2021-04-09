#!/bin/bash

# The generated file in the current working directory
GEN_FILE=xsede-oauth-mapfile
# The real map_file used by services
MAP_FILE=/etc/grid-security/xsede-oauth-mapfile
# The lockfile
MAP_LOCK=./GEN_MAP.LOCK
# The python process for generating the MAP_FILE runs from this directory:
MAP_FILE_BASE=/usr/local/share/utils/xsede_oauth_mapfile

if [ -d $MAP_FILE_BASE ]
then
	cd $MAP_FILE_BASE
else
	# go ahead and linux throw the error
	cd $MAP_FILE_BASE
	exit
fi
cd $MAP_FILE_BASE
if [ -f $MAP_LOCK ]
then
	echo "A map_file generations process is running... exiting"
	exit
fi

# do the update work
touch $MAP_LOCK
./bin/xsede-oauth-mapfile.py

# Try to keep the updates of $MAP_FILE somewhat atomic with cp 
# leveraging linux kernel write buffering
cp -p $GEN_FILE $MAP_FILE
# or alternatively, if you have entries in a master copy map file for
# special cases (multiple local user names, vendor accounts...), 
# you may want to copy and append to that file
#
# cp /pathto/mastermapfile $MAP_FILE; cat mymapfile >> $MAP_FILE

rm $MAP_LOCK
