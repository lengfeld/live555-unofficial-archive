#!/bin/sh

#set -x

archive_name=$1
src=$2

version=$(echo $archive_name | egrep  -o -e "([0-9]{4}\.[0-9]{2}\.[0-9]{2}).tar.gz$" | sed 's/.tar.gz//g')

archive_filename=$(basename $archive_name)

version_long="live.$version"

tagname=v$version-tree

git rev-parse  --verify refs/archives/$tagname >/dev/null 2>&1
if [ $? -eq 0 ] ; then
	echo Tag \'$tagname\' exists already!
	exit 0
fi

echo tagname: $tagname

if [ ! -f "$archive_name" ]; then
	echo "File $archive_name does not exist!"
	exit 1
fi

rm -rf tmp
mkdir tmp

# Create a clean git repo. Otherwise it will overwrite local staged changes in this repo!
(cd tmp && git init -b main && git commit --allow-empty -m "first commit" -q)

(cd tmp && tar xf ../$archive_name)

if [ ! -d tmp/live ]; then
	echo "Archive does not fit file structure. 'live' is missing!"
	exit 1
fi

(cd tmp && git add .)

(cd tmp && git commit -m "dummy commit" -q)

sha1=$(cd tmp && git rev-parse --verify HEAD^{tree})

echo tree $sha1

(cd tmp && GIT_COMMITTER_NAME=live555-unofficial-archive \
	GIT_COMMITTER_EMAIL=invalid@example.com \
	GIT_COMMITTER_DATE=$(echo $version  | sed 's/\./-/g')T00:00:00+00 \
	git tag -a -m "unpack $archive_filename from $src" $tagname $sha1)

git fetch tmp $tagname
git update-ref refs/archives/$tagname FETCH_HEAD

rm -rf tmp
