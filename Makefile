# Minimal makefile for Sphinx documentation

# You can set these variables from the command line:
# e.g. $ make html CYLC_VERSION=1.2.3
CYLC_VERSION = $(shell cylc version | sed 's/Cylc Flow //')
SPHINXOPTS =
SPHINXBUILD = sphinx-build
SOURCEDIR = src
BUILDDIR = doc/$(CYLC_VERSION)

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

clean:
	@$(SPHINXBUILD) -M clean "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

cleanall:
	(cd doc; echo [0-9]*.*)
	rm -rI doc/[0-9]*.*

cli:
	# auto-document CLI reference
	bin/autodoc-cli

.PHONY: help clean cli Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile cli
	# build documentation
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	# write out dict of availabe versions and formats
	bin/write-version-file > doc/versions.json
	# setup HTML redirects to point at this version
	bin/set-default-path "$(CYLC_VERSION)" html
