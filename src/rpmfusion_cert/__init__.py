# rpmfusion-cert - a Python library for Managing rpmfusion SSL Certificates
#
# Copyright (C) 2009-2014 Red Hat Inc.
# Author(s):  Dennis Gilmore <dennis@ausil.us>
#             Ralph Bean <rbean@redhat.com>
#
# RPMFusion version by Sérgio Basto
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version.  See http://www.gnu.org/copyleft/gpl.html for
# the full text of the license.

import os
import getpass
from fedora.client.fas2 import AccountSystem
from fedora.client.fas2 import CLAError
from fedora.client import AuthError
from OpenSSL import crypto
import requests
import datetime
from six.moves import input

# Define our own error class
class rpmfusion_cert_error(Exception):
    pass

def _open_cert():
    """
    Read in the certificate so we dont duplicate the code 
    """
     # Make sure we can even read the thing.
    cert_file = os.path.join(os.path.expanduser('~'), ".rpmfusion.cert")
    if not os.access(cert_file, os.R_OK):
        raise rpmfusion_cert_error("""!!!    cannot read your ~/.rpmfusion.cert file   !!!
!!! Ensure the file is readable and try again !!!""")
    raw_cert = open(cert_file).read()
    my_cert = crypto.load_certificate(crypto.FILETYPE_PEM, raw_cert)
    return my_cert

def verify_cert():
    """
    Check that the user cert is valid. 
    things to check/return
    not revoked
    Expiry time warn if less than 21 days
    """
    if os.path.exists(os.path.expanduser('~/.rpmfusion.upn')):
        print('Kerberos configured, cert ignored')
        return

    my_cert = _open_cert()
    valid_until = my_cert.get_notAfter()[:8].decode()

    dateFmt = '%Y%m%d'
    delta = datetime.datetime.now() + datetime.timedelta(days=21)
    warn = datetime.datetime.strftime(delta, dateFmt)

    print('cert expires: %s-%s-%s' % (valid_until[:4], valid_until[4:6], valid_until[6:8]))

    if valid_until < warn:
        print('WARNING: Your cert expires soon.')

    if hasattr(crypto, 'load_crl'):
        crl_url = "https://admin.fedoraproject.org/ca/crl.pem"
        raw_crl = requests.get(crl_url).content
        crl = crypto.load_crl(crypto.FILETYPE_PEM, raw_crl)
        revoked = crl.get_revoked()
        serial_no = my_cert.get_serial_number()
        if serial_no in [int(cert.get_serial(), 16) for cert in revoked]:
            print('WARNING: Your cert appears in the revocation list.')
            print('        ', crl_url)

def certificate_expired():
    """
    Check to see if ~/.rpmfusion.cert is expired
    Returns True or False

    """
    my_cert = _open_cert()

    if my_cert.has_expired():
        return True
    else:
        return False

def read_user_cert():
    """
    Figure out the Fedora user name from ~/.rpmfusion.cert

    """
    if os.path.exists(os.path.expanduser('~/.rpmfusion.upn')):
        with open(os.path.expanduser('~/.rpmfusion.upn'), 'r') as f:
            return f.read().replace('\n', '')

    my_cert = _open_cert()

    subject = str(my_cert.get_subject())
    subject_line = subject.split("CN=")
    cn_parts = subject_line[1].split("/")
    username = cn_parts[0]
    return username

def create_user_cert(username=None):
    if not username:
        username = input('FAS Username: ')
    password = getpass.getpass('FAS Password: ')
    try:
        fas = AccountSystem('https://admin.rpmfusion.org/accounts/', username=username, password=password)
        cert = fas.user_gencert()
        fas.logout()
    except AuthError:
        raise rpmfusion_cert_error("Invalid username/password.")
    except CLAError:
        fas.logout()
        raise rpmfusion_cert_error("""You must sign the CLA before you can generate your certificate.\n
To do this, go to https://admin.rpmfusion.org/accounts/cla/""")
    cert_file = os.path.join(os.path.expanduser('~'), ".rpmfusion.cert")
    try:
        FILE = open(cert_file,"w")
        FILE.write(cert)
        FILE.close()
    except:
        raise rpmfusion_cert_error("""Can not open cert file for writing.
Please paste certificate into ~/.rpmfusion.cert\n\n%s""" % cert)
