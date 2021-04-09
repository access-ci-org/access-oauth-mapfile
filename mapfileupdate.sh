#!/bin/bash

# The real map_file for Globus-ssh will be placed at MAP_FILE
MAP_FILE=/etc/grid-security/xsede-oauth-mapfile
# The python process for generating the MAP_FILE runs from this directory:
MAP_FILE_GEN=/usr/local/share/utils/xsede_oauth_mapfile
# convenience for the XCI RACD test team :
# MAP_FILE_GEN=./

if [ -d $MAP_FILE_GEN ]
then
	cd $MAP_FILE_GEN
else
	# go ahead and linux throw the error
	cd $MAP_FILE_GEN
	exit
fi
cd $MAP_FILE_GEN
if [ -f ./GENMAP_IN_PROGRESS ]
then
	echo "A map_file generations process is running... exiting"
	exit
fi

# do the update work
touch ./GENMAP_IN_PROGRESS
./xsede-oauth-mapfile.py

# Try to keep the updates of $MAP_FILE somewhat atomic with cp 
# leveraging linux kernel write buffering
cp mymapfile $MAP_FILE
# or alternatively, if you have entries in a master copy map file for
# special cases (multiple local user names, vendor accounts...), 
# you may want to copy and append to that file
#
# cp /pathto/mastermapfile $MAP_FILE; cat mymapfile >> $MAP_FILE

rm ./GENMAP_IN_PROGRESS

