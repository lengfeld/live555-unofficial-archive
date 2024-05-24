
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
	 ls -l archives/all | cut -d" " -f 9- | sort > $@

# TODO Refactorg with build.py. It does not use hardcoded list!
SRCS = gentoo local2023 jog.id.distfiles.macports.org uni-hamburg.de

.PHONY: create-links
create-links:
	./build.py check
	./build.py link

.PHONY: create-tags
create-tags:
	for src in $(SRCS); do \
		for archive in archives/$$src/*.tar.gz; do \
			scripts/unpack.sh $$archive $$src; \
		done \
	done

.PHONY: create-hard
#create-hard: create-tags create-links
# TODO tags do not work correctly yet!
create-hard: create-links


# TODO Find correct way to remove refs in 'refs/archives'
.PHONY: clean-hard
clean-hard:
	for tag in $$(git show-ref | grep archives | cut -d" " -f 2); do git update-ref -d $$tag; done
	rm -f archives/all/*.tar.gz

.PHONY: clean
clean:
	rm -f $(TARGETS)
