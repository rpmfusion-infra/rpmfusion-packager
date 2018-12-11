bin_SCRIPTS = rpmfusion-packager-setup \
              rpmfusion-cert \
              $(NULL)

dist_bin_SCRIPTS = bin/rfabipkgdiff \
                   $(NULL)

CLEANFILES = $(bin_SCRIPTS) \
             Makefile.in \
             aclocal.m4 \
             configure \
             install-sh \
             missing \
             config.status \
             config.log \
             Makefile \
             rpmfusion-packager*.tar.bz2 \
             rpmfusion-packager.spec

EXTRA_DIST = rpmfusion-packager.spec \
             src/rpmfusion-packager-setup.py \
             src/rpmfusion-cert.py \
             $(NULL)

rpmfusion-packager-setup: $(srcdir)/src/rpmfusion-packager-setup.py
	rm -f rpmfusion-packager-setup
	install -p -m 755 -T $(srcdir)/src/rpmfusion-packager-setup.py rpmfusion-packager-setup

rpmfusion-cert: $(srcdir)/src/rpmfusion-cert.py
	rm -f rpmfusion-cert
	install -p -m 755 -T $(srcdir)/src/rpmfusion-cert.py rpmfusion-cert

#
# Link koji-rpmfusion to koji on install
#
install-exec-hook:
	$(LN_S) koji $(DESTDIR)$(bindir)/koji-rpmfusion

rpmfusion_cert_PYTHON = $(wildcard $(srcdir)/src/rpmfusion_cert/*.py)

rpmfusion_certdir = $(pythondir)/rpmfusion_cert

EXTRA_DIST += configs/rpmfusion.conf
kojiconf_DATA = $(srcdir)/configs/rpmfusion.conf
kojiconfdir = $(sysconfdir)/koji.conf.d/

maintainer-clean-local:
	rm -f configure install-sh missing
	rm -f rpmfusion-packager*.tar.bz2
	rm -f autom4te.cache/

rpm: dist-bzip2
	@(rpmbuild -ta rpmfusion-packager-$(PACKAGE_VERSION).tar.bz2)

srpm: dist-bzip2
	@(rpmbuild -ts rpmfusion-packager-$(PACKAGE_VERSION).tar.bz2)
