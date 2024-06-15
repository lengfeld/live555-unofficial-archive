# Internal README

Only for maintaining this repo.

Command to clean and create everything

    $ make clean clean-pub && make checks && make create-pub && make
    $ make clean clean-tags && make checks && make create-tags && make

As one command

    $ make clean clean-pub clean-tags checks && make create-pub create-tags && make

TODO This should be at least one single make command! Refactoring is needed!

## How to publish

Execute the commands

    $ (cd live555-unofficial-git-archive && git push --tags --dry-run)
    $ (cd live555-unofficial-git-archive && git push --tags)
    $ git push --dry-run
    $ git push
