% live555 unofficial archive and mirror

This project is an unofficial archive and mirror of the source code of the
[LIVE555 Streaming Media libraries](http://live555.com/liveMedia/). It collects
the source tarballs released on the server
[live555.com/liveMedia/public/](http://live555.com/liveMedia/public/).


## How to use the archive?

All collected tarballs are listed briefly in the [tarball table](table.html).
For more information for a specific tarball, e.g. including checksums and the
changelog, see the [tarball list](list.html). Both sites contain download
links to the tarballs.


## How to use the git repository?

If you want to work with the code directly in a git repository, please
have a look at
[live555-unofficial-git-archive](https://github.com/lengfeld/live555-unofficial-git-archive).
It's a repository that contains all collected live555 tarballs as git tags and
the tarballs since 2023 as a git commit history.


### Using a git tag with the `-tree` suffix

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


### Using the git commit history and tags without the `-tree` suffix

Since the live555 release `2022-12-01` the tarballs are also committed,
tagged and linked in a commit history. So `git log` does work!

Example usage:

    $ git clone https://github.com/lengfeld/live555-unofficial-git-archive.git
    $ cd live555-unofficial-git-archive
    $ git switch -c main origin/main
    $ git log

The last command shows the history of the live555 releases, including the
changelog in the commit message, until the release `2022-12-01`. This makes it
very easy to see the code changes between the different releases.

Example usage of an tag:

    $ git tag  # Get a list of all tags
    $ git switch --detach v2024.05.15


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

See also this [[Live-devel] older source
archives](http://lists.live555.com/pipermail/live-devel/2011-November/014127.html)
thread on the live555 mailing list for more details about the decisions.


### Are the tarballs authentic?

You will never know for sure! Since the original author does not maintain a
reference archive of the historical source code, you have to rely on third
parties, like this project, to provide the old tarballs. Since the published
tarballs are not signed by the original author, you can only rely on trust.

I can assure that the tarballs I collected should be fine and authentic.
Nevertheless you have to trust me for this. For the other tarballs that are
collected from third parties' archives, like gentoo, you have to trust them.

But the code is open source. Inspecting the code is always possible.


### Is it legal to redistribute the archives?

Yes, it's legal. The original author released the live555 source code under the
[GNU Lesser General Public License (LGPL)](https://www.gnu.org/licenses/lgpl-3.0.html).
This makes it free software and redistributing the source code is allowed.
See also the FAQ entry: [What is the copyright on the source code, and how is it licensed? What are my obligations under this license?](http://www.live555.com/liveMedia/faq.html#copyright-and-license)

And the original author also explicitly states that other websites may keep
older archives and redistribute them.

> I'm not 'hiding' older versions; I'm just not putting them on our web site.
> (Because this is ope source, other people, if they wish, may keep copies of
> older versions, but I'm not.)
> [...]

See [[Live-devel] older source archives](http://lists.live555.com/pipermail/live-devel/2011-November/014131.html).


### What is the expected audience of the mirror?

The expected audience of this website are

* security researchers and
* open source package maintainers

Security researchers should be able to inspect the source code of older live555
releases, e.g. when they investigate an insecure hardware device that ships an
out-of-date version of live555 and other software.

When this site provides stable URLs, also package maintainers for Linux
distributions, like Ubuntu or debian, and maintainers for embedded build
systems, like [openwrt](https://openwrt.org/),
[buildroot](https://buildroot.org/) or [Yocto](https://www.yoctoproject.org/),
can use this site. It provides stable URLs of all the released tarballs that
can be put in build scripts and package recipes.


### Can I use this site as a tarball mirror?

Not yet. For now the links to the live555 tarballs are direct links into the
git repository on github. I don't consider these links as stable. They may
change in the future.

Nevertheless, being a mirror is definitely planned and reasonable. There will be
a single directory that contains all tarballs and has stable links. So it can
be used like other distributions or software project source code archives.

If you need this feature now, please send me an
[email](mailto:stefan+live@lengfeld.xyz).


## Contributions and Questions

The project is hosted on github in the repository
[live555-unofficial-archive](https://github.com/lengfeld/live555-unofficial-archive/).
If you like to contribute, open a PR or create an issue. New sources of
historical tarballs are especially welcomed. The goal of this project is to
have the most complete set of source code archives for live555.

If you have questions, just send me a [mail](mailto:stefan+live@lengfeld.xyz)
or open a [github issue](https://github.com/lengfeld/live555-unofficial-archive/issues/new).


## Prior Art

The need for a live555 tarball backup is also seen by other people. I know of
the following sister projects that also provide an up to date tarball backup:

* [github.com/museoa/live555-backups](https://github.com/museoa/live555-backups)
* [src.rrz.uni-hamburg.de/files/src/live555/](https://src.rrz.uni-hamburg.de/files/src/live555/)
* `http://wex5mlqtzj6mxjwkcugoadlzgwh5qvfuympen2iolo5lep762ramjsqd.onion`
  (Thanks to the maintainer of this project. It's the most extensive and
  historical archive I have found. It contains tarballs as early as 2002!)

The following project adds tarballs as git commits. It uses a github action for automation:

* [github.com/live555-mirror/live555-mirror/](https://github.com/live555-mirror/live555-mirror/)

The following projects added the tarballs as git commits, but updates have
stalled:

* [github.com/rayl/live555](https://github.com/rayl/live555)
  (including the changelog as the commit message)
* [github.com/greenjava/live555](https://github.com/greenjava/live555)


## Imprint

This website is created and maintained by

* name: Stefan Lengfeld
* address: Germany, 53721 Siegburg
* e-mail: [stefan+live@lengfeld.xyz](mailto:stefan+live@lengfeld.xyz)
* website: [stefan.lengfeld.xyz](https://stefan.lengfeld.xyz)

The source code of this wobsite and all tools for mirroring can be found at
[github.com/lengfeld/live555-unofficial-archive](https://github.com/lengfeld/live555-unofficial-archive).
