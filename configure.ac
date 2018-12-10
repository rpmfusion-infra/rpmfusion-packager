AC_INIT([rpmfusion-packager],[0.6.3])
AM_INIT_AUTOMAKE([dist-bzip2 no-dist-gzip])
AC_PATH_PROGS(PYTHON, python3)
AM_PATH_PYTHON([3],, [:])
AM_CONDITIONAL([HAVE_PYTHON3], [test "$PYTHON" != :])
AC_PATH_PROGS(BASH, sh bash)
AC_PROG_LN_S

AC_CONFIG_FILES([
Makefile
rpmfusion-packager.spec
])

AC_OUTPUT
