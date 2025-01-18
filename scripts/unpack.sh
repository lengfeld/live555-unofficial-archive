#!/bin/sh
# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2024 Stefan Lengfeld <stefan@lengfeld.xyz>

set -e

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

previous_version=$1  # can also be the string "NONE"
current_version=$2
src=$3   # for current version
do_trees=$4
do_commits=$5
changelog_text="$6"

archive_name="live.$current_version.tar.gz"
archive_path="srcs/$src/$archive_name"
archive_filename=$(basename $archive_name)

version_long="live.$current_version"

tagname=v$current_version

# Check whether the tags already exists
GIT_DIR=$REPO_DIR git rev-parse --verify refs/tags/$tagname-tree >/dev/null 2>&1 && true
if [ $? -eq 0 ] ; then
	do_trees="no"
	echo Info: Tag \'$tagname-tree\' exists already!
fi

GIT_DIR=$REPO_DIR git rev-parse --verify refs/tags/$tagname >/dev/null 2>&1 && true
if [ $? -eq 0 ] ; then
	do_commits="no"
	echo Info: Tag \'$tagname\' exists already!
fi

if [ "$do_commits" = "no" -a "$do_trees" = "no" ]; then
	echo Info: Scripts end. Nothing to do for version $current_version!
	exit 0
fi

# Some additional checks
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

# Strip toplevel 'live' folder while unpack
(cd tmp && tar xf ../$archive_path --strip-components=1)

# Use "--force" to ignore global git config on ignore files
(cd tmp && git add --force .)

# Create a commit object without a parent for this tree
date=$(echo $current_version | sed 's/\./-/g')T00:00:00+00
(cd tmp && GIT_COMMITTER_NAME=live555-unofficial-archive \
	GIT_COMMITTER_EMAIL=invalid@example.com \
	GIT_COMMITTER_DATE=$date \
	GIT_AUTHOR_NAME="Live Networks, Inc" \
	GIT_AUTHOR_EMAIL=invalid@example.com \
	GIT_AUTHOR_DATE=$date \
	git commit -m "unpack $archive_filename from $src" -m "Copyright (c), Live Networks, Inc.  All rights reserved" -q)

tree_sha1=$(cd tmp && git rev-parse -q --verify HEAD^{tree})

echo $tree_sha1

if [ "$do_trees" = "yes" ]; then
	# Append the suffix "-tree" to the tagname.  The tag points to a commit
	# that has no parents. So the commit only references the tree.  Not the
	# tree plus the history of the tree/repo. In the history of the
	# live555-unofficial-archive this was the first tag variant.
	(cd tmp && GIT_COMMITTER_NAME=live555-unofficial-archive \
		GIT_COMMITTER_EMAIL=invalid@example.com \
		GIT_COMMITTER_DATE=$date \
		git tag -a -m "live555 $current_version from $src" $tagname-tree HEAD)
fi

# Now create commit with history
if [ "$do_commits" = "yes" ]; then
	if [ "$previous_version" != "NONE" ]; then
		# Fetch the existing previous version from the other git
		# repository into the temporary git repo.
		(cd tmp && git fetch ../$REPO_DIR v$previous_version)
		(cd tmp && git switch -c main-new FETCH_HEAD^{commit})
	else
		(cd tmp && git switch --orphan main-new)
		# There is no previous version for the history. Create a
		# initial empty commit!
		# NOTE: This uses the same date as the first tarball here.
		(cd tmp && GIT_COMMITTER_NAME=live555-unofficial-archive \
			GIT_COMMITTER_EMAIL=invalid@example.com \
			GIT_COMMITTER_DATE=$date \
			GIT_AUTHOR_NAME="Unrelevant author" \
			GIT_AUTHOR_EMAIL=invalid@example.com \
			GIT_AUTHOR_DATE=$date \
			git commit -q -m "initial empty commit" --allow-empty)
	fi

	# First throw away files in the working tree and index. Otherwise the
	# next command does not fully reset all files to $tree_sha1. I have
	# seen some left over files from previous commits.
	(cd tmp && git rm -r . || true)
	(cd tmp && git checkout -f $tree_sha1 .)

	# Create commit object
	(cd tmp && GIT_COMMITTER_NAME=live555-unofficial-archive \
		GIT_COMMITTER_EMAIL=invalid@example.com \
		GIT_COMMITTER_DATE=$date \
		GIT_AUTHOR_NAME="Live Networks, Inc" \
		GIT_AUTHOR_EMAIL=invalid@example.com \
		GIT_AUTHOR_DATE=$date \
		git commit -q -m "unpack $archive_filename" \
			-m "Copyright (c), Live Networks, Inc.  All rights reserved." \
			-m "Changelog:" \
			-m "$changelog_text")

	# Create tag object
	(cd tmp && GIT_COMMITTER_NAME=live555-unofficial-archive \
		GIT_COMMITTER_EMAIL=invalid@example.com \
		GIT_COMMITTER_DATE=$date \
		git tag -a -m "live555 $current_version" $tagname HEAD)
fi

# Push tags and commits
if [ "$do_trees" = "yes" ]; then
	GIT_DIR=$REPO_DIR git fetch tmp $tagname-tree
	GIT_DIR=$REPO_DIR git update-ref refs/tags/$tagname-tree FETCH_HEAD
fi
if [ "$do_commits" = "yes" ]; then
	GIT_DIR=$REPO_DIR git fetch tmp $tagname
	GIT_DIR=$REPO_DIR git update-ref refs/tags/$tagname FETCH_HEAD
	GIT_DIR=$REPO_DIR git fetch tmp  main-new
	GIT_DIR=$REPO_DIR git update-ref refs/heads/main FETCH_HEAD
fi

rm -rf tmp
