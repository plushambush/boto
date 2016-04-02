.PHONY: clean sources srpm tests

DIST       ?= epel-6-x86_64
PROJECT    ?= boto
PACKAGE    := python-$(PROJECT)
VERSION    := $(shell rpm -q --qf "%{version}\n" --specfile $(PACKAGE).spec | head -1)
RELEASE    := $(shell rpm -q --qf "%{release}\n" --specfile $(PACKAGE).spec | head -1)

GIT        := $(shell which git)

ifdef GIT
SHA := $(shell git rev-parse --short --verify HEAD)
TAG := $(shell git show-ref --tags -d | grep $(SHA) |\
	git name-rev --tags --name-only $$(awk '{ print $2 }'))
endif

sources: clean
ifndef TAG
	$(eval SHA_DATE :=  $(shell git show -s --format=%ci $(SHA)))
	$(eval BUILDID  := .$(shell date --date='$(SHA_DATE)' '+%Y%m%d%H%M').git$(SHA))
	$(eval BUILDREG := "s/(%define[[:space:]]*buildid[[:space:]]*).*/\\1$(BUILDID)/i")
	@git cat-file -p $(SHA):$(PACKAGE).spec | sed -r -e $(BUILDREG) > $(PACKAGE).spec
endif
	@git archive --format=tar --prefix="$(PROJECT)-$(VERSION)/" \
		$(shell git rev-parse --verify HEAD) | gzip > $(PROJECT)-$(VERSION).tar.gz

srpm: sources
	@mkdir -p srpms/
	@rpmbuild -bs --define "_sourcedir $(CURDIR)" \
		--define "_srcrpmdir $(CURDIR)/srpms" $(PACKAGE).spec

ifdef TAG
rpm:
	@mkdir -p rpms/$(DIST)
	/usr/bin/mock -r $(DIST) \
		--rebuild srpms/$(PACKAGE)-$(VERSION)-$(RELEASE).src.rpm \
		--resultdir rpms/$(DIST)

copr: srpm
	@copr-cli build --nowait c2devel/c2-sdk \
		srpms/$(PACKAGE)-$(VERSION)-$(RELEASE).src.rpm
endif

tests:
	@tox

clean:
	@rm -rf build dist srpms rpms $(PROJECT).egg-info $(PROJECT)-*.tar.gz *.egg
