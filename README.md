# live555 unofficial archive

This project is an unofficial archive of the source code of the [LIVE555
Streaming Media libraries](http://live555.com/liveMedia/).


## How to use it?

All collected tarballs are in the folder [archives/all](archives/all). There
you can download the archives and use them.


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

You will never know for sure! Since the original auther does not maintain a
reference archive of the historical source code, you have to rely on third
parties, like this project, to provide the old tarballs. Since the published
tarballs are not signed by the original author, you can only rely on trust.

I can assure that the tarballs I collected should be fine and authentic.
Nevertheless you have to trust me for this. For the other tarballs, that are
collected from third parties archives, like gentoo, you have to trust them.


## Contributions

If you like to contribute, open a PR or create an issue. Especially new sources
of historical tarballs are welcome. The goal of this project is to have the
most complete set of source code archives for live555.


## TODOs

Add tarballs as tag/tree/commit objects to a git repository. The code is
already there, but the usability is currently bad and must be fixed.

Search the wayback machine for tarballs and add them.

Find more public tarballs and add them.

Include the `changelog.txt` and add a list of all existing live555 library
versions.
