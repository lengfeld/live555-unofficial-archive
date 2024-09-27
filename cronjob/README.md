# Archive getter and cronjob

## How to develop

Just run

    $ make tests

## How to deploy

Add the following line to our crontab

    32 * * * * cd ~/git/live555-unofficial-archive/cronjob/data/ && ../watcher.py get http://live555.com/liveMedia/public/

to run the script every hour.

## Discussion/Questions

### Design question

Actually I would write now a function to serialize an deserialize the
FileInfos list to a string/text file and back.
Current choice would be to dump the stuff as json. While loading the fields
would be checked and it would be converted back to FileInfo namedtuples.

This is the canonical way.

Questions: Why not use the pickle functionality?
-> bad reputation, binary format (cannot be easily debugged and constructed "by hand")

Question why not just use the html itself?


### Where to put the tests

Currently I have the tests in the same file.  For non-compiled languages this
means, that on every program invocation the test code is also parsed on the
test modules are also imported.

Is this bad for performance or permature optimization.

Sometimes the tests cannot be in the same file. E.g. for scripts as programs
that are invoked from the shell.

Update: This is not true. Even for a program the tests can be in the same file.
The python script must be called with

     $ python3 -m unittest diff_file_infos

Then the tests from the test class are executed and not the main function!

But it needs to contain the trick

    if __name__ == "__main__":
        sys.exit(main())

for libraries!
