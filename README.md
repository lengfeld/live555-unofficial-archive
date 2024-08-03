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

Execute the commands

    $ (cd live555-unofficial-git-archive && git push --tags --dry-run)
    $ (cd live555-unofficial-git-archive && git push --tags)
    $ git push --dry-run
    $ git push

TODO add commands to publish gh-pages!


## TODOs

Add my cronjob watcher script to continously polls the live555 download page.

Search the wayback machine for tarballs and add them.

Get tarballs from videolan
(https://download.videolan.org/pub/contrib/live555/). Check for vlc specific
modifications.

Find more public tarballs and add them.

Add distributions to the prior art list

Get grid of `pub/archives` but include checksums!
