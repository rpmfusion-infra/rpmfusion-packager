AC_INIT([rpmfusion-packager],[0.6.2])
AM_INIT_AUTOMAKE([dist-bzip2 no-dist-gzip])
AC_PATH_PROGS(PYTHON, python)
AM_CONDITIONAL([HAVE_PYTHON], [test "$PYTHON" != :])
AM_PATH_PYTHON(,, [:])
AC_PATH_PROGS(BASH, sh bash)
AC_PROG_LN_S

AC_CONFIG_FILES([
Makefile
rpmfusion-packager.spec
])

AC_OUTPUT
