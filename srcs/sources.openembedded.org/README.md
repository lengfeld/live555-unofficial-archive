Found this mirror in the thread of

     https://lists.openembedded.org/g/openembedded-core/topic/72142842

See http://sources.openembedded.org/

How to get all live555 tarballs

    $ mkdir get
    $ cd get
    $ wget http://sources.openembedded.org/  # get index page

    # get live555 tarballs from all the files:
    $ grep 'href="live.[^"]*"' -o index.html  | cut -c 7- | sed 's/"//g' > files.txt

    # Download all tarballs and md5 sum files
    $ for line in $(cat files.txt); do wget http://sources.openembedded.org/$line ; done 

    # Check the md5sum files manually. Some
    #     'no properly formatted checksum lines found'
    # errors

    # Cleanup and finish
    $ rm files.txt  index.html
    $ md5sum *.tar.gz > files.md5
    $ mv * ../
    $ cd ..
    $ rmdir get

Date: 2024-08-05
