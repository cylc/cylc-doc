# Minimal makefile for Sphinx documentation

# You can set these variables from the command line:
# e.g. $ make html CYLC_VERSION=1.2.3
CYLC_VERSION = $(shell cylc version | sed 's/Cylc Flow //')
SPHINXOPTS = -n
SPHINXBUILD = sphinx-build
SOURCEDIR = src
BUILDDIR = doc/$(CYLC_VERSION)
STABLE = true  # Makes this the Stable and default build
LATEST = true  # Makes this the Latest build
# The Stable/default build is what you get when navigating to the docs root dir
# For pre-release (except nightly) builds, set STABLE=false LATEST=true

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

clean:
	@$(SPHINXBUILD) -M clean "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	# remove auto-generated content
	rm -rf src/plugins/main-loop/built-in
	rm -rf src/plugins/install/built-in
	rm -rf src/user-guide/task-implementation/job-runner-handlers

cleanall:
	(cd doc; echo [0-9]*.*)
	rm -rI doc/[0-9]*.*

.PHONY: help clean Makefile .EXPORT_ALL_VARIABLES

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
# NOTE: EXPORT_ALL_VARIABLES exports make vars as env vars
%: Makefile .EXPORT_ALL_VARIABLES
	# build documentation
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	# write out dict of available versions and formats
	bin/version write > doc/versions.json
	# Redirect doc/<version>/index.html -> doc/<version>/html/index.html
	bin/create-html-redirect "html/index.html" "$(BUILDDIR)/index.html"
	# Redirect old pages
	bin/redirect-old-pages
ifeq ($(STABLE),true)  # makefile conditionals in recipe must be unindented
	# Link e.g. doc/stable/ -> doc/7.0/
	rm "$(BUILDDIR)/../stable" || true
	ln -sr "$(BUILDDIR)" "$(BUILDDIR)/../stable"
	# Redirect doc/index.html -> doc/stable/index.html
	bin/create-html-redirect "stable/index.html" "$(BUILDDIR)/../index.html"
endif
ifeq ($(LATEST),true)
	# Link e.g. doc/latest/ -> doc/8.0a1/
	rm "$(BUILDDIR)/../latest" || true
	ln -sr "$(BUILDDIR)" "$(BUILDDIR)/../latest"
endif
