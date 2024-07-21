Downloaded the tarballs from the mirror

    https://src.rrz.uni-hamburg.de/files/src/live555/

with the commands

    $ rm *.tar.gz
    $ wget -l 1 -r  https://src.rrz.uni-hamburg.de/files/src/live555/
    $ mv src.rrz.uni-hamburg.de/object/*/*.tar.gz  ./
    $ mv live.2016.06.23.tar.gz dir && mv dir/live555-latest.tar.gz live.2016.06.23.tar.gz && rmdir dir
    $ md5sum *.tar.gz > files.md5
    $ rm -rf src.rrz.uni-hamburg.de/

If found this mirror in the git repo https://github.com/museoa/live555-backups

Date: 2024-05-24
