I downloaded these files from

    http://jog.id.distfiles.macports.org/macports/distfiles/live555/

with the following commands

    $ wget -l 1 -r http://jog.id.distfiles.macports.org/macports/distfiles/live555/
    $ rm *.tar.gz
    $ mv jog.id.distfiles.macports.org/macports/distfiles/live555/*.tar.gz ./
    $ rm -rf jog.id.distfiles.macports.org
    $ m5sum -c files.md5
    $ md5sum *.tar.gz > files.md5

Done at 2024-05-19.

Update 2024-08-05: The mirror site

    http://www.mirrorservice.org/sites/distfiles.macports.org/live555/

contains the same files. Found by googleing.
