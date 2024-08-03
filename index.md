# live555 unofficial archive

This project is an unofficial archive of the source code of the [LIVE555
Streaming Media libraries](http://live555.com/liveMedia/). It collects
the source tarballs released on the server
[live555.com/liveMedia/public/](http://live555.com/liveMedia/public/).


## How to use it?

All collected tarballs are listed briefly in the [tarball table](table.html).
For more information for a specific tarball, e.g. including checksums and the
changelog, see the [tarball list](list.html). Both sites contain download
links to the tarballs.

If you want to work with the code directly in a git repository, please
have a look at
[live555-unofficial-git-archive](https://github.com/lengfeld/live555-unofficial-git-archive).
It's a repository that contains all collected live555 tarballs.

Example usage:

    $ git clone https://github.com/lengfeld/live555-unofficial-git-archive.git
    $ cd live555-unofficial-git-archive
    $ git tag  # list all versions/tags
    $ git diff v2024.04.19-tree v2024.05.05-tree  # compare two versions

    # Checkout the source code without creating a branch
    $ git switch --detach v2024.04.19-tree

_Note_: The tags have the suffix `-tree`. The git tags point to commit objects
without a history. They only contain the file contents of the tarballs. So `git
log` does not work!


## Frequently Ask Questions

### Why was this project created?

The original author of the libraries does not maintain historical versions of
the source code. The reasons are stated in the
[FAQ](http://live555.com/liveMedia/faq.html#no-source-code-repository):

> Why do you not make the code available under a 'source code repository'?
>
> Unlike some other open source projects, the source code for this project is
> provided as a 'tarball', rather than in a source code repository - because
> old versions of the code are not supported. (A source code repository might
> also encourage developers to extend the source code by modifying it 'in
> place' (and then upgrading the code by 'merging diffs'). As noted above,
> modifying the supplied code 'in place' is something that we discourage;
> instead, developers should use C++ subclassing to extend the code.)

I can follow the reasoning that only the newest and current version is
supported. That's a fair decision.

Nevertheless I also value traceability. This means that you can follow the
development process. E.g. when a bug was fixed or a feature was introduced.
This can only achieved if you have a development history as a source code
repository or historical archives.  Relying on third parties for this goal has
a couple of issues.


### Are the tarballs authentic?

You will never know for sure! Since the original author does not maintain a
reference archive of the historical source code, you have to rely on third
parties, like this project, to provide the old tarballs. Since the published
tarballs are not signed by the original author, you can only rely on trust.

I can assure that the tarballs I collected should be fine and authentic.
Nevertheless you have to trust me for this. For the other tarballs, that are
collected from third parties archives, like gentoo, you have to trust them.

But the code is open source. Inspecting the code is always possible.

### Can I use this site as a tarball mirror?

Not yet. For now the links to the live555 tarballs are direct links into the
git repository on github. I don't consider these links as stable. They may
change in the future.

Nevertheless it is definitely planed and reasonable. There will be a single
directory that contains all tarballs and has stable links. So it can be used
like other distributions or software project source code archives.

If you need this feature now, please send me an [email](mailto:stefan+live@lengfeld.xyz).


## Contributions and Questions

The project is hosted on github in the repository
[live555-unofficial-archive](https://github.com/lengfeld/live555-unofficial-archive/).
If you like to contribute, open a PR or create an issue. Especially new sources
of historical tarballs are welcome. The goal of this project is to have the
most complete set of source code archives for live555.

If you have questions, just send me a [mail](mailto:stefan+live@lengfeld.xyz)
or open a [github issue](https://github.com/lengfeld/live555-unofficial-archive/issues/new).


## Prior Art

The need for a live555 tarball backup is also seen by other people. I know of
the following sister projects that also provide an up to date tarball backup:

* [github.com/museoa/live555-backups](https://github.com/museoa/live555-backups)
* [src.rrz.uni-hamburg.de/files/src/live555/](https://src.rrz.uni-hamburg.de/files/src/live555/)

The following project added the tarballs including the changelog text as git commits:

* [github.com/rayl/live555](https://github.com/rayl/live555)


## Impressum

This website is created and maintained by

* name: Stefan Lengfeld
* address: Germany, 53721 Siegburg
* e-mail: [stefan+live@lengfeld.xyz](mailto:stefan+live@lengfeld.xyz)
