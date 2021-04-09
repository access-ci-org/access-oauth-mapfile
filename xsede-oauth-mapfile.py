#!/usr/bin/env python
"""
Generate an oauth compatible map_file for use with oAuth SSH

See: https://github.com/XSEDE/oauth-ssh/blob/master/server/README.md 
for a description of the map_file and discussion of how it may be used.

Galen Arnold, XSEDE,  July 2019
"""

# To setup XA-API-KEY in the .json config file, see:
# https://xsede-xdcdb-api.xsede.org  , and all the tabs there, especially:
#  -> Request Headers
#  -> Generate API-KEY

# here to keep pylint happy with print()
from __future__ import print_function
import json
import re
import requests
MYCONFIGFILE="xsede-oauth-mapfile-config.json"
MYMAPFILE="mymapfile"


def read_configuration(config_file):
    """
    Read the configuration file and return a tuple of the values.
    """
    print("reading config_file:", config_file)
    myconfig = json.loads(config_file.read())
    xa_agent = myconfig['XA-AGENT']
    xa_resource = myconfig['XA-RESOURCE']
    xa_api_key = myconfig['XA-API-KEY']
    return (xa_agent, xa_resource, xa_api_key)


def auth_test(xa_agent, xa_resource, xa_api_key):
    """
    Check the auth_test and json handling via requests
    """
    print("testing authentication, should return 200...")
    myresult = requests.get('https://xsede-xdcdb-api.xsede.org/userinfo/auth_test',

        headers={'XA-AGENT':xa_agent,
                 'XA-RESOURCE':xa_resource,
                 'XA-API-KEY':xa_api_key})
    print(myresult, "\n")
    if (not(re.search("200",str(myresult),flags=0))):
        print ("Authentication with xdcdb-api-test failed.\n")
        exit()
    

def gen_mapfile(xa_agent, xa_resource, xa_api_key, output_file):
    """
    Make the real query and generate a mapfile
    """
    print("generating {} for:".format(output_file))
    myurl = "https://xsede-xdcdb-api.xsede.org/"
    myurl += "userinfo/v1/resources/usernames/"
    myurl += xa_resource
    myresult = requests.get(myurl,
                            headers={'XA-AGENT':xa_agent,
                                     'XA-RESOURCE':xa_resource,
                                     'XA-API-KEY':xa_api_key})
    mydata = myresult.json()

    print("   XA-RESOURCE: {}".format(mydata['result']['resource']))
    print("\nThe following entries mapping to multiple local accounts")
    print("\"portalLogin localaccta localacctb\" WERE written to {}.\n".format(MYMAPFILE))
  
    i = 0
    for somebody in mydata['result']['users']:
        # if there are multiple usernames,
        # make a note of it but don't write to mapfile
        if len(somebody['usernames']) > 1:
             multilocalstring = somebody['portalLogin']
             for name in somebody['usernames']:
                 multilocalstring += " " + name
                 output_file.write("{}@xsede.org {}\n".
                                   format(somebody['portalLogin'],
                                          name))
             print(multilocalstring)
        else:
            output_file.write("{}@xsede.org {}\n".
                              format(somebody['portalLogin'],
                                     somebody['usernames'][0]))
            i = i + 1
    print("\nlines written to {}: {}\n".format(MYMAPFILE,i))


def main():
    """
    main program

    """
    config_file = open(MYCONFIGFILE, "r")
    (xa_agent, xa_resource, xa_api_key) = read_configuration(config_file)
    config_file.close()

    auth_test(xa_agent, xa_resource, xa_api_key)

    output_file = open(MYMAPFILE, "w")
    gen_mapfile(xa_agent, xa_resource, xa_api_key, output_file)
    output_file.close()


main()
