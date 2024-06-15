#!/bin/sh

#set -x

REPO_DIR=live555-unofficial-git-archive/.git/

# Learnings: tagged tree objects
# Git allows to create a tag object for any other object, e.g. tree objects.
# Normally it's only for commit objects. The linux kernel contains also a tag object
# that points to a tree object.
#  https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tag/?h=v2.6.11-tree
# E.g. this sometimes works, e.g. `git diff tag1 tag2` works with these kind
# of objects.
# Nevertheless not everything works. E.g. you cannot execute `git checkout
# tag1` if the tag1 object points to a tree object.
#   $ git checkout  refs/archives/v2023.05.10-tree
#   fatal: Cannot switch branch to a non-commit 'refs/archives/v2023.05.10-tree'
# Solution: Even when it's not logically (because it has no parrent), create an
# additional commit object.

version=$1
src=$2

archive_name="live.$version.tar.gz"
archive_path="srcs/$src/$archive_name"
archive_filename=$(basename $archive_name)

version_long="live.$version"

# Append the suffix "-tree" to the tagname.  The tag points to a commit that
# has no parents. So the commit only references the tree.  No the tree plus the
# history of the tree/repo.
tagname=v$version-tree

GIT_DIR=$REPO_DIR git rev-parse --verify refs/tags/$tagname >/dev/null 2>&1
if [ $? -eq 0 ] ; then
	echo Tag \'$tagname\' exists already!
	exit 0
fi

echo tagname: $tagname

if [ ! -f "$archive_path" ]; then
	echo "File $archive_path does not exist!"
	exit 1
fi

rm -rf tmp
mkdir tmp

# Create a clean git repo. Otherwise it will overwrite local staged changes in this repo!
(cd tmp && git init -b main)

# Check tar archive. It must contain a toplevel folder "live" and nothing more
# at the top level!
if [ "$(tar tf $archive_path | cut -d/ -f 1 | sort | uniq)" != "live" ]; then
	echo "ERROR: tar archive is more then 'live' at the toplevel"
	echo ""
	exit 1
fi

# Strip toplevel 'live' folder
(cd tmp && tar xf ../$archive_path --strip-components=1)

(cd tmp && git add .)

date=$(echo $version  | sed 's/\./-/g')T00:00:00+00
(cd tmp && GIT_COMMITTER_NAME=live555-unofficial-archive \
	GIT_COMMITTER_EMAIL=invalid@example.com \
	GIT_COMMITTER_DATE=$date \
	GIT_AUTHOR_NAME="Live Networks, Inc." \
	GIT_AUTHOR_EMAIL=invalid@example.com \
	GIT_AUTHOR_DATE=$date \
	git commit -m "unpack $archive_filename from $src" -m "Copyright (c), Live Networks, Inc.  All rights reserved" -q)

(cd tmp && GIT_COMMITTER_NAME=live555-unofficial-archive \
	GIT_COMMITTER_EMAIL=invalid@example.com \
	GIT_COMMITTER_DATE=$date \
	git tag -a -m "live555 $version from $src" $tagname HEAD)

# TODO combine to a single command
GIT_DIR=$REPO_DIR git fetch tmp $tagname
GIT_DIR=$REPO_DIR git update-ref refs/tags/$tagname FETCH_HEAD

rm -rf tmp
