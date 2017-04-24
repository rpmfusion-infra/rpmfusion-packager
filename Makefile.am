bin_SCRIPTS = rpmfusion-packager-setup \
	 $(NULL)

CLEANFILES = $(bin_SCRIPTS) Makefile.in \
    aclocal.m4 \
	configure \
	install-sh \
	missing \
	config.status \
	config.log \
	Makefile \
	rpmfusion-packager*.tar.gz \
	rpmfusion-packager.spec

EXTRA_DIST = \
    rpmfusion-packager.spec \
    src/rpmfusion-packager-setup.py \
	src/secondary-koji

rpmfusion-packager-setup: $(srcdir)/src/rpmfusion-packager-setup.py
	rm -f rpmfusion-packager-setup
	install -p -m 755 -T $(srcdir)/src/rpmfusion-packager-setup.py rpmfusion-packager-setup

install-exec-local:
	cd $(DESTDIR)/usr/bin; rm -f koji-rpmfusion; $(LN_S) koji koji-rpmfusion

EXTRA_DIST += configs/rpmfusion.conf
kojiconf_DATA = $(srcdir)/configs/rpmfusion.conf
kojiconfdir = $(sysconfdir)/koji.conf.d/

maintainer-clean-local:
	rm -f configure install-sh missing
	rm -f rpmfusion-packager*.tar.bz2
	rm -f autom4te.cache/

rpm: dist-gzip
	@(rpmbuild -ta rpmfusion-packager-$(PACKAGE_VERSION).tar.gz)

srpm: dist-gzip
	@(rpmbuild -ts rpmfusion-packager-$(PACKAGE_VERSION).tar.gz)
