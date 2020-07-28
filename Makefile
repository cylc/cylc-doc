# Minimal makefile for Sphinx documentation

# You can set these variables from the command line:
# e.g. $ make html CYLC_VERSION=1.2.3
CYLC_VERSION = $(shell cylc version | sed 's/Cylc Flow //')
SPHINXOPTS = -n
SPHINXBUILD = sphinx-build
SOURCEDIR = src
BUILDDIR = doc/$(CYLC_VERSION)
SETCURRENT = true

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

clean:
	@$(SPHINXBUILD) -M clean "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	# remove auto-generated content
	rm -rf src/user-guide/plugins/main-loop/built-in

cleanall:
	(cd doc; echo [0-9]*.*)
	rm -rI doc/[0-9]*.*

.PHONY: help clean Makefile .EXPORT_ALL_VARIABLES

default_version =
ifeq ($(SETCURRENT),true)
	default_version = current
endif

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
# NOTE: EXPORT_ALL_VARIABLES exports make vars as env vars
%: Makefile .EXPORT_ALL_VARIABLES
	# build documentation
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	# write out dict of available versions and formats
	bin/version write > doc/versions.json
	# setup HTML redirects to point at this version if $(SETCURRENT) == true
	bin/set-default-path "$(BUILDDIR)" "$(CYLC_VERSION)" html "$(default_version)"
