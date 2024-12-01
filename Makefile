
TARGETS += checks/git.show.tags checks/git.ls-tree.tags checks/git.ls-remote
TARGETS += checks/git.log.main checks/git.log.main-readme
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

# TODO maybe use 'raw' also for other checks
checks/git.log.main:
	(cd live555-unofficial-git-archive && git log main --format=raw) > $@

checks/git.log.main-readme:
	(cd live555-unofficial-git-archive && git log main-readme --format=raw) > $@

checks/links.all:
	(cd pub/archives && ls -l live* | cut -c 38- ) | sort > $@

.PHONY: checks
checks:
	./build.py check
	./build.py check_git_tags


.PHONY: lint
lint:
	pycodestyle *.py

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

# TODO This also creates the main branch
.PHONY: create-tags
create-tags:
	./build.py tag

.PHONY: clean-checks
clean-checks:
	rm -rf checks
	mkdir checks


.PHONY: clean-hard
clean-tags:
	cd live555-unofficial-git-archive && \
		for tag in $$(git tag); do git tag -d $$tag; done && \
		(git branch -D main || true)


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


# NOTE: This only works if there are uncommitted changes to the website (=the
# gh-pages) branch.
# NOTE: These commands are just tuned for my local setup.
.PHONY: page
page: pub/index.html pub/list.html pub/table.html
	git worktree add gh-pages origin/gh-pages
	(cd gh-pages && \
		git branch -D gh-pages && \
		git branch gh-pages origin/gh-pages && \
		git rm * && \
		touch .nojekyll && \
		cd .. && cp $^ gh-pages/ && cd gh-pages && \
		git add * .nojekyll && \
		git commit -m "update gh-pages" && \
		git branch -D gh-pages && \
		git branch gh-pages $$(git rev-parse HEAD) && \
		echo "summary:" && git diff origin/gh-pages gh-pages --compact-summary && \
		echo show changes: git diff origin/gh-pages gh-pages); \
	git worktree remove --force gh-pages

DRY_RUN=--dry-run

# Push two branches, new tags and one branch
.PHONY: publish
publish:
	git push origin main gh-pages $(DRY_RUN)
	cd live555-unofficial-git-archive && git push origin main --tags $(DRY_RUN)

.PHONY: clean
clean:
	rm -f $(TARGETS) -r build/
