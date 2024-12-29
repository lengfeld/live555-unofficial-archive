#!/bin/sh
# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2024 Stefan Lengfeld <stefan@lengfeld.xyz>
#
# Script to generate the branch 'main-readme' in the repo
# live555-unofficial-git-archive bit-to-bit identical.
#
# Show existing history with all the details
#    $ git log --pretty=fuller --date=iso main-readme

set -e

export GIT_COMMITTER_EMAIL=stefan@lengfeld.xyz
export GIT_AUTHOR_NAME="Stefan Lengfeld"
export GIT_AUTHOR_EMAIL=stefan@lengfeld.xyz

git switch --orphan main-readme

# First commit
export GIT_COMMITTER_DATE="2024-05-26 21:17:11 +0200"
export GIT_AUTHOR_DATE="2024-05-26 21:17:07 +0200"
git commit -m "Initial commit" --allow-empty

# Second commit
cat >README.md <<EOF
# live555 unofficial git archive

See [live555-unofficial-archive](https://github.com/lengfeld/live555-unofficial-archive)
for details.
EOF
export GIT_COMMITTER_DATE="2024-05-26 21:18:34 +0200"
export GIT_AUTHOR_DATE="2024-05-26 21:16:37 +0200"
git add README.md
git commit -m "add README.md"

# Third Commit
cat >README.md <<EOF
# live555 unofficial git archive

To see all tags, clone the repository and execute \`git tag\`. Or visit the
[tags page on github](https://github.com/lengfeld/live555-unofficial-git-archive/tags).

See [live555-unofficial-archive](https://github.com/lengfeld/live555-unofficial-archive)
for more details.
EOF
export GIT_COMMITTER_DATE="2024-06-15 23:14:50 +0200"
export GIT_AUTHOR_DATE="2024-06-15 23:11:36 +0200"
git add README.md
git commit -m "Add info how to find the tags"

# Fourth Commit
cat >README.md <<EOF
# live555 unofficial git archive

To see all tags, clone the repository and execute \`git tag\`. Or visit the
[tags page on github](https://github.com/lengfeld/live555-unofficial-git-archive/tags).

See [live555-unofficial-archive](https://lengfeld.github.io/live555-unofficial-archive/)
for more details.
EOF
export GIT_COMMITTER_DATE="2024-08-03 02:40:43 +0200"
export GIT_AUTHOR_DATE="2024-08-03 02:40:43 +0200"
git add README.md
git commit -m "redirect to gh-pages"

# Fifth commit
cat >README.md <<EOF
# live555 unofficial git archive

To see all tags, clone the repository and execute \`git tag\`. Or visit the
[tags page on github](https://github.com/lengfeld/live555-unofficial-git-archive/tags).

To see the live555 releases since \`2022-12-01\` as a commit history, see the
[main](https://github.com/lengfeld/live555-unofficial-git-archive/commits/main)
branch.

See [live555-unofficial-archive](https://lengfeld.github.io/live555-unofficial-archive/)
for more details.
EOF
export GIT_COMMITTER_DATE="2024-12-09 10:48:00 +0100"
export GIT_AUTHOR_DATE="2024-12-09 10:46:45 +0100"
git add README.md
git commit -m "add note about commit history"
