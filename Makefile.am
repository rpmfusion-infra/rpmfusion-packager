bin_SCRIPTS = rpmfusion-free-cvs rpmfusion-nonfree-cvs rpmfusion-packager-setup plague-client-rf
CLEANFILES = $(bin_SCRIPTS) Makefile.in aclocal.m4
EXTRA_DIST = \
    rpmfusion-packager.spec \
    src/rpmfusion-free-cvs.py \
    src/rpmfusion-nonfree-cvs.py \
    src/rpmfusion-packager-setup.py \
    src/plague-client-rf.sh

rpmfusion-free-cvs: $(srcdir)/src/rpmfusion-free-cvs.py
	rm -f rpmfusion-free-cvs
	cp -p $(srcdir)/src/rpmfusion-free-cvs.py rpmfusion-free-cvs
	chmod ugo+x rpmfusion-free-cvs

rpmfusion-nonfree-cvs: $(srcdir)/src/rpmfusion-nonfree-cvs.py
	rm -f rpmfusion-nonfree-cvs
	cp -p $(srcdir)/src/rpmfusion-nonfree-cvs.py rpmfusion-nonfree-cvs
	chmod ugo+x rpmfusion-nonfree-cvs

rpmfusion-packager-setup: $(srcdir)/src/rpmfusion-packager-setup.py
	rm -f rpmfusion-packager-setup
	cp -p $(srcdir)/src/rpmfusion-packager-setup.py rpmfusion-packager-setup
	chmod ugo+x rpmfusion-packager-setup

plague-client-rf: $(srcdir)/src/plague-client-rf.sh
	rm -f plague-client-rf
	cp -p $(srcdir)/src/plague-client-rf.sh plague-client-rf
	chmod ugo+x plague-client-rf

maintainer-clean-local:
	rm -f configure install-sh missing
	rm -f rpmfusion-packager*.tar.bz2

rpm: dist
	@(rpmbuild -ta rpmfusion-packager-$(PACKAGE_VERSION).tar.bz2)

srpm: dist
	@(rpmbuild -ts rpmfusion-$(PACKAGE_VERSION).tar.bz2)
