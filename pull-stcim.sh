#!/bin/sh

set -e
set -x

# The old manual instructions were:
#
#     Download new archives
#
#         $ rsync -av --dry-run stcim.de:git/live555-mirror/getter/crontab-test2/ stcimde/
#         $ rsync -av stcim.de:git/live555-mirror/getter/crontab-test2/ stcimde/
#
#     Compare changelogs
#
#         $ vimdiff stcimde/2024-09-20T07:32:01+0000/changelog.txt ../../changelog.txt
#         $ cp stcimde/2024-09-20T07:32:01+0000/changelog.txt ../../changelog.txt
#
#     copy all tars again into place
#
#         $ find stcimde/  -name "live\.*.tar.gz" | xargs -I test cp test ./
#
#     Remove one that is too much
#
#         $ rm live.2023.11.30.tar.gz
#
#     now regenerate. See README.md
#
# These are converted to this script

if [ ! -d srcs/localgetter ]; then
	echo "executed from the wrong directory!"
	exit 1
fi

cd srcs/localgetter/

rsync -av stcim.de:~/git/live555-unofficial-archive/cronjob/data/ stcimde/

latest_folder=$(ls -1 stcimde/ | grep -v state | sort  | tail -n 1)

# Update changelog
cp stcimde/$latest_folder/changelog.txt ../../changelog.txt

# Update missing tarballs
for tarball_path in stcimde/*/live.*.tar.gz; do
	tarball_filename=$(basename $tarball_path)

	# Only copy not yet copied tarballs
	test -f $tarball_filename && continue

	# Special case: Skip this old tarball.
	[ "live.2023.11.30.tar.gz" = "$tarball_filename" ] && continue

	echo New tarball: $tarball_path
	cp $tarball_path ./
done

echo "Now continue with regenerating"
