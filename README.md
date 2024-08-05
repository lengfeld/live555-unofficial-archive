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

    # generate: also geenerate all tags
    $ make clean clean-pub checks clean-tags && make create-pub create-tags && make && make page

    # Review changes and maybe add fixes.
    $ git diff
    # Then regenerate

    # Commit the final result

    #

    $ (cd live555-unofficial-git-archive && git push --tags --dry-run)
    $ (cd live555-unofficial-git-archive && git push --tags)
    $ git push --dry-run
    $ git push

TODO rework the above section

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
