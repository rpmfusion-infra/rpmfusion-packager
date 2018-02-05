#!/usr/bin/python
# fedora-cert - a command line tool to manage your fedora SSL user certificates
#
# Copyright (C) 2009-2014 Red Hat Inc.
# Author(s):  Dennis Gilmore <dennis@ausil.us>
#             Ralph Bean <rbean@redhat.com>
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version.  See http://www.gnu.org/copyleft/gpl.html for
# the full text of the license.

import optparse
import fedora_cert
import os.path
import sys

def main(opts):
    # lets read in the existing cert if it exists.
    # gets us existing acc info
    if not opts.username:
        try:
            username = fedora_cert.read_user_cert()
        except:
            print("Can't determine fas name, lets get a new cert")
            try:
                fedora_cert.create_user_cert(None)
            except fedora_cert.fedora_cert_error as e:
                print(e)
                sys.exit(1)
            sys.exit(0)
    else:
        username = opts.username

    if opts.confkrb:
        with open(os.path.expanduser('~/.fedora.upn'), 'w') as f:
            f.write(username)
        print('Kerberos username configured. Run kinit %s@FEDORAPROJECT.ORG' %
              username)
        sys.exit(0)

    #has cert expired? do we force a new cert? get a new one
    if opts.newcert:
        print("Getting a new User Certificate")
        try:
            fedora_cert.create_user_cert(username)
        except fedora_cert.fedora_cert_error as e:
            print(e)
            sys.exit(1)
        sys.exit(0)
    if fedora_cert.certificate_expired():
        print("Certificate has expired, getting a new one")
        try:
            fedora_cert.create_user_cert(username)
        except fedora_cert.fedora_cert_error as e:
            print(e)
            sys.exit(1)
        sys.exit(0)
    if opts.verifycert:
        print("Verifying Certificate")
        try:
            fedora_cert.verify_cert()
        except fedora_cert.fedora_cert_error as e:
            print(e)
            sys.exit(1)

        import OpenSSL.crypto
        if not hasattr(OpenSSL.crypto, 'load_crl'):
            print("CRL Checking not available in this version of pyOpenSSL")

if __name__ == '__main__':
    opt_p = optparse.OptionParser(usage="%prog [OPTIONS] ")
    opt_p.add_option('-u', '--username', action='store', dest='username',
                     default=False, help="FAS Username.")
    opt_p.add_option('-n', '--new-cert', action='store_true', dest='newcert',
                     default=False, help="Generate a new Fedora Certificate.")
    opt_p.add_option('-v', '--verify-cert', action='store_true', dest='verifycert',
                     default=False, help="Verify Certificate.")
    opt_p.add_option('-k', '--configure-krb', action='store_true', dest='confkrb',
                     default=False, help="Configure krb5.")

    (opts, args) = opt_p.parse_args()

    main(opts)
