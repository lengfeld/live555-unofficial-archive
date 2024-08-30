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

How to add new tarballs

    $ git add srcs/<new source>

    # generate: only add new tarballs
    $ make clean clean-pub checks && make create-pub create-tags && make && make page

    # generate: also regenerate all tags
    $ make clean clean-pub checks clean-tags && make create-pub create-tags && make && make page

    # Review changes and maybe add fixes.
    $ git diff
    # Then regenerate

    # Commit the final result
    $ git add [...]
    $ git commit -m "add new src and tarballs"

    $ Publish the result
    $ make page
    # Review the changes with "git diff"

    $ git push origin <commit>:gh-pages --dry-run
    $ git push origin main --dry-run

    # Publish new git tags
    $ (cd live555-unofficial-git-archive && git push --tags --dry-run)

    # NOTE: Remove the "--dry-run" after check/test

To publish only the gh-pages, execute

    $ make clean clean-pub checks && make create-pub && make && make page

and then execute the `git push` command to the branch `gh-pages`. And then
commit the local changes and also push them.


## TODOs

Add my cronjob watcher script to continously polls the live555 download page.

Search the wayback machine for tarballs and add them.

Get tarballs from videolan
(https://download.videolan.org/pub/contrib/live555/). Check for vlc specific
modifications.

Find more public tarballs and add them.

Add distributions/mirrors to the prior art list

Get grid of `pub/archives` but include checksums!

Define and implement public "API" for tarball mirror.

Include the list of sources on the gh-pages website.

Add custom pandoc template to make the pages stylestyle the same.

Looking at https://code.google.com/archive/p/live555sourcecontrol/source/default/commits
https://code.google.com/archive/p/live555sourcecontrol/

See also the mailing list messages. Add to documentation
http://lists.live555.com/pipermail/live-devel/2011-November/014127.html

Also look at https://github.com/live555-mirror/live555-mirror

Also look at https://github.com/rgaufman/live555

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
