#!/usr/bin/python
# -*- coding: utf-8 -*-
#  Copyright (C) 2009 Stewart Adam
#  Copyright (C) 2007, 2008, 2009 Dennis Gilmore
#  This file is part of rpmfusion-packager.

#  rpmfusion-packager is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.

#  rpmfusion-packager is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

#  You should have received a copy of the GNU General Public License
#  along with rpmfusion-packager.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys
import pycurl
import subprocess

def download(location, file):
    """Save data at location to file. WARNING: Overwrites files!"""
    fh = open(file, 'w')
    curl = pycurl.Curl()
    curl.setopt(pycurl.URL, location)
    curl.setopt(pycurl.FOLLOWLOCATION, 1)
    curl.setopt(pycurl.MAXREDIRS, 5)
    curl.setopt(pycurl.CONNECTTIMEOUT, 30)
    curl.setopt(pycurl.TIMEOUT, 300)
    curl.setopt(pycurl.NOSIGNAL, 1)
    curl.setopt(pycurl.WRITEDATA, fh)
    curl.setopt(pycurl.SSL_VERIFYPEER, False)
    try:
        curl.perform()
        fh.close()
    except:
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.stderr.flush()
        # remove the empty file
        os.remove(file)
    curl.close()

if __name__ == "__main__":
    USERHOME = os.path.expanduser('~')
    print 'Setting up RPM Fusion packager environment'
    if not os.path.isfile(os.path.join(USERHOME, '.rpmfusion.user')):
        username = raw_input('Enter your RPM Fusion username: ')
        fh = open(os.path.join(USERHOME, '.rpmfusion.user'), 'w')
        fh.write(username)
        fh.close()
    else:
      print "~/.rpmfusion.user already exists - skipping"
    if not os.path.isfile(os.path.join(USERHOME, '.rpmfusion.cert')):
        print "You need a client certificate from the RPM Fusion Account System"
        print "Please download one from https://admin.rpmfusion.org/accounts/user/gencert"
        print "Save it to ~/.rpmfusion.cert and re-run this script"
        sys.exit(1)
    if not os.path.isfile(os.path.join(USERHOME, '.rpmfusion-upload-ca.cert')):
        print 'Retrieving .rpmfusion-upload-ca.cert'
        download('https://admin.rpmfusion.org/accounts/rpmfusion-upload-ca.cert',
                 '%s/.rpmfusion-upload-ca.cert' % USERHOME)
    else:
      print '~/.rpmfusion-upload-ca.cert already exists - skipping'
    if not os.path.isfile(os.path.join(USERHOME, '.rpmfusion-server-ca.cert')):
        print 'Retrieving .rpmfusion-server-ca.cert'
        download('https://admin.rpmfusion.org/accounts/rpmfusion-server-ca.cert',
                 '%s/.rpmfusion-server-ca.cert' % USERHOME)
    else:
        print '~/.rpmfusion-server-ca.cert already exists - skipping'
print 'Done!'
