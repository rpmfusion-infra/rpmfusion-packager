AC_INIT([rpmfusion-packager],[0.7.1])
AM_INIT_AUTOMAKE([dist-bzip2 no-dist-gzip])
AC_PATH_PROGS(BASH, sh bash)
AC_PROG_LN_S

AC_ARG_WITH([python3],
        AS_HELP_STRING([--with-python3], [build for Python 3 (default)]),
        [], [with_python3=unset])

AC_ARG_WITH([python2],
        AS_HELP_STRING([--with-python2], [build for Python 2]),
        [with_python3=no], [with_python2=unset])

AS_IF([test "x$with_python3" != xno],
      	[AM_PATH_PYTHON([3])],
	[AS_IF([test "x$with_python2" = xyes], [AM_PATH_PYTHON([2.7])],)])

AC_CONFIG_FILES([
Makefile
rpmfusion-packager.spec
src/rpmfusion-packager-setup.py
src/rpmfusion-cert.py
])

AC_SUBST_FILE([changelog])
changelog=$srcdir/ChangeLog
AC_OUTPUT
