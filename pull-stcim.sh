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

cp stcimde/$latest_folder/changelog.txt ../../changelog.txt
git add ../../changelog.txt

# only supports getting one tarball, not all the non-integrated ones
tarball_filename=$(cd stcimde/$latest_folder/ && ls live.*.tar.gz)
cp stcimde/$latest_folder/$tarball_filename  ./
git add $tarball_filename

echo "Now continue with regenerating"
