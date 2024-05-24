
#TARGETS += checks/git.show.tags checks/git.show-ref.tags
TARGETS += checks/links.all

all: $(TARGETS)

# TODO Avoid "grep archives"!!!
checks/git.show.tags:
	for tag in $$(git show-ref | grep archives | cut -d" " -f 1); do git show $$tag; echo ----; done > $@

# TODO Avoid "| grep achives". Find out of the refspec for show-ref works!!
checks/git.show-ref.tags:
	git show-ref --dereference | grep archives > $@

checks/links.all:
	 ls -l pub/archives | cut -d" " -f 12- | sort > $@

# TODO Refactor with build.py. It does not use hardcoded list!
SRCS = gentoo local2023 jog.id.distfiles.macports.org uni-hamburg.de

.PHONY: checks
checks:
	./build.py check

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

.PHONY: create-tags
create-tags:
	for src in $(SRCS); do \
		for archive in srcs/$$src/*.tar.gz; do \
			scripts/unpack.sh $$archive $$src; \
		done \
	done


# TODO Find correct way to remove refs in 'refs/archives'
.PHONY: clean-hard
clean-hard:
	#for tag in $$(git show-ref | grep archives | cut -d" " -f 2); do git update-ref -d $$tag; done
	rm -rf pub

.PHONY: clean
clean:
	rm -f $(TARGETS)
