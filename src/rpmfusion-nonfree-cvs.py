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
import subprocess
#from OpenSSL import crypto

def readUser():
    """Sample line "Subject: C=US, ST=North Carolina, O=RPM Fusion Project, OU=Full Name, CN=user/emailAddress=user@domain.com"""
    # FIXME: We're not using this style of cert yet. When we do, remove this
    #        comment and change the function accordingly.
    CERT_LOC = os.path.join(os.path.expanduser('~'), '.rpmfusion.cvsuser')
    try:
        user = open(CERT_LOC, 'r').read().strip()
    except IOError:
        print "Error: Cannot read your ~/.rpmfusion.cvsuser file! Using anonymous CVS."
        user = None
    return user # skip the below until we change cert contents
    # -----
    CERT_LOC = os.path.join(os.path.expanduser('~'), '.rpmfusion.cert')
    userCert = ""
    if os.access(CERT_LOC, os.R_OK):
        userCert = open(CERT_LOC, 'r').read()
    else:
        print "Error: Cannot read your ~/.rpmfusion.cert file! Using anonymous CVS."
        return None
    myCert = crypto.load_certificate(1, userCert)
    if myCert.has_expired():
        print "Error: Your certificate has expired! Please get a new one at fas.rpmfusion.org"
        sys.exit(1)
    subject = str(myCert.get_subject())
    subjectLine = subject.split("CN=")
    name = subjectLine[1].split("/")
    return name[0]

def cvsco(user, module):
    """Checks out module in cvs as user (nonfree repo)"""
    print "*** Checking out %s from RPM Fusion CVS (nonfree repo) as %s:" % (module, user or 'anonymous')
    environment = os.environ
    if user:
      environment['CVSROOT'] = ':ext:%s@cvs.rpmfusion.org:/cvs/nonfree/' % user
    else:
      environment['CVSROOT'] = ':pserver:anonymous@cvs.rpmfusion.org:/cvs/nonfree/'
    environment['CVS_RSH'] = 'ssh'
    retval = subprocess.Popen("cvs co %s" % module, shell=True, env=environment).wait()
    if retval != 0:
        sys.exit(1)

def usage(error=None):
    if error:
        print 'Error: %s' % error
    else:
        print 'Checkout modules from RPM Fusion CVS (nonfree repo)'
    print """Usage: rpmfusion-nonfree-cvs [module list]
  -h, --help: Show this help message.
  -a, --anonymous: Use anonymous CVS.

Example: rpmfusion-nonfree-cvs comps owners xorg-x11-drv-nvidia"""

if __name__ == '__main__':
    anonymous = False
    try:
        import getopt
        (opts, pkgs) = getopt.getopt(sys.argv[1:], "ha", ['help', 'anonymous'])
    except (getopt.GetoptError), error:
        usage(error)
        sys.exit(1)
    for (opt, value) in opts:
        if opt in ['-h', '--help']:
            usage()
            sys.exit(1)
        elif opt in ['-a', '--anonymous']:
            anonymous = True
    if not pkgs:
      usage('You must specify one or more modules to checkout.')
      sys.exit(1)
    if anonymous:
      user = None
    else:
      user = readUser()
    for pkg in pkgs:
        cvsco(user, pkg)

