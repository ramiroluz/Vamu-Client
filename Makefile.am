## Process this file with automake to produce Makefile.in
## Created by Anjuta

SUBDIRS = src 

vamu_clientdocdir = ${prefix}/doc/vamu_client
vamu_clientdoc_DATA = \
	README\
	COPYING\
	AUTHORS\
	ChangeLog\
	INSTALL\
	NEWS


EXTRA_DIST = $(vamu_clientdoc_DATA)


# Remove doc directory on uninstall
uninstall-local:
	-rm -r $(vamu_clientdocdir)
