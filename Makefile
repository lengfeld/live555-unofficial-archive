
TARGETS += checks/git.show.tags checks/git.ls-remote checks/git.ls-tree.tags
TARGETS += checks/links.all

all: $(TARGETS)

checks/git.show.tags:
	(cd live555-unofficial-git-archive && \
		for tag in $$(git tag); do git show --no-patch $$tag; echo ----; done) > $@

checks/git.ls-tree.tags:
	(cd live555-unofficial-git-archive && \
		for tag in $$(git tag); do git ls-tree --name-only -r $$tag; done) | sort | uniq > $@

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
	./build.py list > pub-tmp/list.html
	./build.py table > pub-tmp/table.html
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

# TODO Cleanup the build and pub folder mess!
build:
	mkdir -p $@

build/index.html: index.md build
	pandoc --toc -s -f markdown -t html $< -o $@

pub/index.html: build/index.html
	cp $< $@

.PHONY:
page: pub/index.html pub/list.html pub/table.html
	git worktree add gh-pages origin/gh-pages
	(cd gh-pages && \
		git rm * && \
		touch .nojekyll && \
		cd .. && cp $^ gh-pages/ && cd gh-pages && \
		git add * .nojekyll && \
		git commit -m "update gh-pages" && \
		echo git push origin $$(git rev-parse HEAD):gh-pages --dry-run); \
	git worktree remove --force gh-pages


.PHONY: clean
clean:
	rm -f $(TARGETS) -r build/
