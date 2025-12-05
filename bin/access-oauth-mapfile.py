#!/usr/bin/env python3
"""
Generates an OAuth compatible map_file for use with GCS, OAuth SSH, and other services

Galen Arnold, JP Navarro, Eric Blau
"""

# To setup XA-API-KEY in the .json config file, see:
# https://allocations-api.access-ci.org/acdb/, and all the tabs there, especially:
#  -> Request Headers
#  -> Generate APIKEY

import argparse
import http.client as httplib
import json
import logging
import logging.handlers
import os
import pdb
import pwd
import signal
import ssl
import sys
from urllib.parse import urlparse

# Used during initialization before loggin is enabled
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

class Generate_Mapfile():
    def __init__(self):
        # Parse arguments
        parser = argparse.ArgumentParser()
        parser.add_argument('-l', '--log', action='store', \
                            help='Logging level (default=info)')
        parser.add_argument('-c', '--config', action='store', dest='config', required=False, \
                            help='Configuration file', default='etc/access-oauth-mapfile-config.json')
        parser.add_argument('-m', '--mapfile', action='store', dest='mapfile', required=False, \
                            help='Map file name', default='access-oauth-mapfile')
        parser.add_argument('-u', '--url', action='store', dest='apiurl', required=False, \
                            help='Base URL of the spacct API server')
        parser.add_argument('-t', '--test', action='store_true', \
                            help='Only run an Auth test')
        parser.add_argument('--pdb', action='store_true', \
                            help='Run with the Python debugger')
        parser.add_argument('-s', '--stdout', action='store_true', dest='stdout', required=False, \
                            help='Use stdout', default=False)
        parser.add_argument('-r', '--resource', action='store', dest='resource', required=False, \
                            help='Resource to query', default=False)
        self.args = parser.parse_args()

        # Trace for debugging as early as possible
        if self.args.pdb:
            pdb.set_trace()

        # Load configuration file
        config_path = os.path.abspath(self.args.config)
        try:
            with open(config_path, 'r') as file:
                conf=file.read()
        except IOError as e:
            eprint('Error "{}" reading config={}'.format(e, config_path))
            sys.exit(1)
        try:
            self.config = json.loads(conf)
        except ValueError as e:
            eprint('Error "{}" parsing config={}'.format(e, config_path))
            sys.exit(1)

        if not self.config.get('XA-AGENT'):
            eprint('Config is missing XA-AGENT')
            sys.exit(1)
            
        if not self.config.get('XA-RESOURCE'):
            eprint('Config is missing XA-RESOURCE')
            sys.exit(1)

        if not self.config.get('XA-API-KEY'):
            eprint('Config is missing XA-API-KEY')
            sys.exit(1)
            
    def Setup(self):
        # Initialize log level from arguments, or config file, or default to WARNING
        loglevel_str = (self.args.log or self.config.get('LOG_LEVEL', 'INFO')).upper()
        loglevel_num = getattr(logging, loglevel_str, None)
        self.logger = logging.getLogger('CronLog')
        self.logger.setLevel(loglevel_num)
        self.formatter = logging.Formatter(fmt='%(asctime)s.%(msecs)03d %(levelname)s %(message)s', \
                                           datefmt='%Y/%m/%d %H:%M:%S')
        self.LOG_FILE = self.config.get('LOG_FILE', 'var/access-oauth-mapfile.log')
        self.handler = logging.handlers.TimedRotatingFileHandler(self.LOG_FILE, \
            when='W6', backupCount=999, utc=True)
        self.handler.setFormatter(self.formatter)
        self.logger.addHandler(self.handler)

        signal.signal(signal.SIGINT, self.exit_signal)
        signal.signal(signal.SIGTERM, self.exit_signal)

        mode = 'test' if self.args.test else 'normal'
        self.logger.critical('Starting mode=({}), program={}, pid={}, uid={}({})'.format(mode, os.path.basename(__file__), os.getpid(), os.geteuid(), pwd.getpwuid(os.geteuid()).pw_name))
        
        self.API_HEADERS = {'XA-AGENT': self.config.get('XA-AGENT'),
             'XA-RESOURCE': self.config.get('XA-RESOURCE'),
             'XA-API-KEY': self.config.get('XA-API-KEY')}
        apiurl = self.args.apiurl
        if not apiurl:
            self.API_HOST = 'allocations-api.access-ci.org' 
            self.API_PATH = '/acdb/'
        else:
            url = urlparse(apiurl)
            if not url.netloc:
                self.API_HOST = 'allocations-api.access-ci.org' 
            else:
                self.API_HOST = url.netloc 
            if not url.path:
                self.API_PATH = '/acdb/'
            else:
                self.API_PATH = url.path 

        # If no resource is specified on the command line, use the MAP-RESOURCE
        self.RESOURCE = self.args.resource or self.config.get('MAP-RESOURCE') or self.config.get('XA-RESOURCE')

    def exit_signal(self, signum, frame):
        self.logger.critical('Caught signal={}({}), exiting with rc={}'.format(signum, signal.Signals(signum).name, signum))
        sys.exit(signum)
        
    def exit(self, rc):
        if rc:
            self.logger.error('Exiting with rc={}'.format(rc))
        sys.exit(rc)

    def Auth_Test(self):
        """
        Check the Auth_Test and json handling via requests
        """
        ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        conn = httplib.HTTPSConnection(host=self.API_HOST, port=443, context=ctx)
        conn.request('GET', self.API_PATH+"/spacct/auth_test", None, self.API_HEADERS)
        response = conn.getresponse()
        if response.status != 200:
            self.logger.critical('Authentication with {} FAILED.'.format(self.API_HOST))
            self.exit(1)
        self.logger.info('Authentication with {} PASSED.'.format(self.API_HOST))
        myresult = response.read().decode("utf-8-sig")
        return(0)

    def Fallback_to_XSEDE(self):
        """
        Query the XSEDE server as a fallback
        """
        import datetime
        self.logger.critical('Falling back to querying XSEDE server.')
        access_onset = datetime.date(2022,9,1)
        today = datetime.date.today()
        if today >= access_onset:
            self.logger.critical('XSEDE has ended, cannot fall back to XSEDE server.')
            self.exit(1)

        ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        conn = httplib.HTTPSConnection(host='allocations-api.access-ci.org', port=443, context=ctx)
        conn.request('GET', '/spacct/v1/users/resource/{}'.format(self.RESOURCE), None, self.API_HEADERS)
        response = conn.getresponse()
        if response.status != 200:
            self.logger.critical('Falling back to XSEDE server failed. Response was {}'.format(response.reason))
            self.exit(1)

        return(response)
       

    def Generate_Mapfile(self):
        """
        Make the real query and generate a mapfile
        """
        ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        conn = httplib.HTTPSConnection(host=self.API_HOST, port=443, context=ctx)
        conn.request('GET', self.API_PATH+'/spacct/v2/users/resource/{}'.format(self.RESOURCE), None, self.API_HEADERS)
        response = conn.getresponse()
        if response.status != 200:
            self.logger.critical('Connection to {} failed. response was {}'.format(self.API_HOST,response.reason))
            response = self.Fallback_to_XSEDE()
        myresult = response.read().decode("utf-8-sig")
        mydata = json.loads(myresult)

        MAPFILE = self.args.mapfile
        USE_STDOUT = self.args.stdout
        USER_COUNT = 0
        MAP_COUNT = 0
        try:
            #with open(MAPFILE, 'w') as output_file:
            output_file = sys.stdout if USE_STDOUT else open(MAPFILE, 'w') 
            for user in mydata['result']['users']:
                for name in user['usernames']:
                    output_file.write('{}@access-ci.org {}\n'.format(user['portalLogin'], name))
                    MAP_COUNT += 1
                USER_COUNT += 1
            if output_file is not sys.stdout:
                output_file.close()
        except IOError as e:
            self.logger.critical('Error "{}" writing mapfile={}'.format(e, MAPFILE))
            sys.exit(1)
        self.logger.info('Wrote users={}, maps={}'.format(USER_COUNT, MAP_COUNT))
        return(0 if USER_COUNT > 0 else 1)

if __name__ == '__main__':
    program = Generate_Mapfile()
    rc = program.Setup()
    if program.args.test:
        rc = program.Auth_Test()
    else:
        rc = program.Generate_Mapfile()
    program.exit(rc)
