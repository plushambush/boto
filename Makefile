.PHONY: clean sources srpm tests

PROJECT    ?= boto
PACKAGE    := python-$(PROJECT)
VERSION    := $(shell rpm -q --qf "%{version}\n" --specfile $(PACKAGE).spec | head -1)

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
	@rpmbuild -bs --define "_sourcedir $(CURDIR)" \
		--define "_srcrpmdir $(CURDIR)" $(PACKAGE).spec

tests:
	@tox

clean:
	@rm -rf build dist $(PROJECT).egg-info $(PROJECT)-*.tar.gz *.egg *.src.rpm
