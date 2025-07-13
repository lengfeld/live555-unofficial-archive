# live555 unofficial archive - source

This repository contains the source of the
[live555 unofficial archive](https://lengfeld.github.io/live555-unofficial-archive/) project.
Please see there or in [index.md](index.md) for further details.

This is only the internal README of the project.


## Maintaining

Command to clean and create everything

    $ make clean clean-pub && make checks && make create-pub && make
    $ make clean clean-tags && make checks && make create-tags && make

As one command

    $ make clean clean-pub clean-tags checks && make create-pub create-tags && make

TODO This should be at least one single make command! Refactoring is needed!

To only include new tarballs, execute

    $ make clean clean-pub checks && make create-pub create-tags && make && make page

It's faster but does not created existing git tags.

Then publish the gh-pages. The previous commands prints a `git push` command.


## How to publish

How to add new tarballs from 'localgetter':

    $ ./pull-stcim.sh

    # check the result: tarball and changelog changes
    $ git status

    # generate: only add new tarballs
    $ make clean clean-pub checks && make create-pub create-tags && make && make page

    # Review changes
    $ git diff

    # add all new stuff and commit
    $ git add pub/ srcs/localgetter/*.tar.gz checks/ changelog.txt

    # Commit the final result
    $ git commit -a -m "add new tarball"

    # And publish with
    $ make publish
    # And then remove the --dry-run options
    $ make publish DRY_RUN=


## How to rebuild the git repo `live555-unofficial-git-archive`

The instructions are

    $ rm -rf live555-unofficial-git-archive
    $ git init live555-unofficial-git-archive
    $ (cd live555-unofficial-git-archive && \
        git remote add origin git@github.com:lengfeld/live555-unofficial-git-archive.git)
    $ make create-branch-readme-main
    $ make create-tags

And check that the repo has the same state/info as before:

    $ rm checks/git.ls-remote
    $ make checks/git.ls-remote


## TODOs

Search the wayback machine for tarballs and add them.

Get tarballs from videolan
(https://download.videolan.org/pub/contrib/live555/). Check for vlc specific
modifications.

Find more public tarballs and add them.

Add distributions/mirrors to the prior art list

Get grid of `pub/archives` but include checksums!

Define and implement public "API" for tarball mirror.

Add custom pandoc template to make the pages stylestyle the same.

Looking at https://code.google.com/archive/p/live555sourcecontrol/source/default/commits
https://code.google.com/archive/p/live555sourcecontrol/

See also the mailing list messages. Add to documentation
http://lists.live555.com/pipermail/live-devel/2011-November/014127.html

Also look at https://github.com/live555-mirror/live555-mirror
- DONE: added as prior art
- TODO: integrated into srcs and checks

Maybe add as prior art
* https://github.com/rgaufman/live555
* https://github.com/verkada/live555
But it has changes on top the original source code

Optimize webpage for the "mirror" term for SEO.
* There is no keyword information whether archive or mirror is the better
  search term.
* Use the domain "live555-mirror.net".

Check files in tar archives against files in git tags

    $ for file in pub/archives/*.tar.gz; do tar tf $file ; done | sort | uniq  > x

Watch stack overflow for live555 mirror questions.

Publish cmake file

Add compile tests

The function "choose_preferred_src()" does not scale. There should be at best
no references to the srcs anywhere. And a table for the final link between
tarballs and the prefer src for backwards compatibility.

Add RSS feed for new archives

Allow to regenerate the whole 'live555-unofficial-git-archive' git repo. For
now everything can be generated execpt the 'main-readme' branch.

Add scripts to update other srcs, without redownloading all files existing files.
