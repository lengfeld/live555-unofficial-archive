
TARGETS += checks/git.show.tags checks/git.ls-remote checks/git.ls-tree.tags
TARGETS += checks/links.all

all: $(TARGETS)

checks/git.show.tags:
	(cd live555-unofficial-git-archive && \
		for tag in $$(git tag); do git show --no-patch $$tag; echo ----; done) > $@

checks/git.ls-tree.tags:
	(cd live555-unofficial-git-archive && \
		for tag in $$(git tag); do git ls-tree --name-only -r $$tag; done) | sort | uniq -c> $@

checks/git.ls-remote:
	git ls-remote live555-unofficial-git-archive/ > $@

checks/links.all:
	 ls -l pub/archives | cut -d" " -f 13- | sort > $@

.PHONY: checks
checks:
	./build.py check

# TODO This build arragement is bad. It does not use dependencies to avoid
# rebuilding and recomputing (e.g. the checksums).
pub:
	rm -rf pub-tmp
	mkdir -p pub-tmp/archives
	./build.py link
	./build.py versions > pub-tmp/versions.txt
	cd pub-tmp/archives && \
		md5sum *.tar.gz > checksums.md5 && \
		sha256sum *.tar.gz > checksums.sha256 && \
		sha512sum *.tar.gz > checksums.sha512
	rm -rf pub
	mv pub-tmp pub

.PHONY: create-pub
create-pub: pub

.PHONY: create-tags
create-tags:
	./build.py tag


.PHONY: clean-hard
clean-tags:
	cd live555-unofficial-git-archive && \
		for tag in $$(git tag); do git tag -d $$tag; done

.PHONY: clean-pub
clean-pub:
	rm -rf pub

.PHONY: clean
clean:
	rm -f $(TARGETS)
