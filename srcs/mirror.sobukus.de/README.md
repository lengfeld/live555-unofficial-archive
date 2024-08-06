Found the site

    http://mirror.sobukus.de/files/src/live555/

For some tarballs the mirror references the 

    https://src.rrz.uni-hamburg.de/

mirror. But it seems that this mirror contains more tarballs.

Getting all tarballes

    $ wget -l 1 -r  http://mirror.sobukus.de/files/src/live555/
    $ find  mirror.sobukus.de/object/ -type f | xargs -I test mv "test" ./
    $ rm -rf mirror.sobukus.de/

And yes it contains at lot of (+20) new tarballes.

Added 2024-08-06
