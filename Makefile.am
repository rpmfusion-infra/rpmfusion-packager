bin_SCRIPTS = rpmfusion-packager-setup \
	rpmfusion-free-cvs \
	rpmfusion-nonfree-cvs \
	rpmfusion-koji

CLEANFILES = $(bin_SCRIPTS) Makefile.in \
    aclocal.m4 \
	configure \
	install-sh \
	missing \
	config.status \
	config.log \
	Makefile \
	rpmfusion-packager*.tar.bz2 \
	rpmfusion-packager.spec

EXTRA_DIST = \
    rpmfusion-packager.spec \
    src/rpmfusion-free-cvs.py \
    src/rpmfusion-nonfree-cvs.py \
    src/rpmfusion-packager-setup.py \
	src/secondary-koji

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
	install -p -m 755 -T $(srcdir)/src/rpmfusion-packager-setup.py rpmfusion-packager-setup

rpmfusion-koji: $(srcdir)/src/secondary-koji
	rm -f rpmfusion-koji
	install -p -m 755 -T $(srcdir)/src/secondary-koji rpmfusion-koji

EXTRA_DIST += configs/rpmfusion-config
kojiconf_DATA = $(srcdir)/configs/rpmfusion-config
kojiconfdir = $(sysconfdir)/koji

maintainer-clean-local:
	rm -f configure install-sh missing
	rm -f rpmfusion-packager*.tar.bz2
	rm -f autom4te.cache/

rpm: dist-gzip
	@(rpmbuild -ta rpmfusion-packager-$(PACKAGE_VERSION).tar.gz)

srpm: dist-gzip
	@(rpmbuild -ts rpmfusion-packager-$(PACKAGE_VERSION).tar.gz)
