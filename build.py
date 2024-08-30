#!/usr/bin/env python3

import os
import sys
import fnmatch
from os.path import join
from subprocess import run
from enum import Enum

# NOTE: All paths are hard coded. It must be executed in the top level
# directory of the repo.


def is_potential_version_line(line):
    if len(line) == 0:
        return False
    # Special cases:
    if line.startswith("8-bit u-l"):
        return False
    elif line.startswith("2002.08.29 release, a"):
        return False
    return line[0].isdigit()


def is_line_with_version(line):
    if fnmatch.fnmatch(line, '????.??.??:'):
        # Normal cases
        return True
    elif fnmatch.fnmatch(line, '????-??-??:'):
        # New format since 2024-03-08:
        return True
    elif fnmatch.fnmatch(line, '????.??.??[a-b]:'):
        return True
    elif line == "2012.08.08":  # special case without colon
        return True
    elif line == "2003:03;11:":  # special case
        return True
    return False


# The version should look like "2012.08.08" or "2003.02.03b"
def normalize_version(line):
    line = line.rstrip(":")
    line = line.replace("-", ".")

    # Special case
    if line == "2003:03;11":
        line = "2003.03.11"

    # Check
    if not (fnmatch.fnmatch(line, '????.??.??[a-b]') or fnmatch.fnmatch(line, '????.??.??')):
        raise Exception("Version number is not normal: %s" % (line,))

    return line


# Generator
def parse_changelog(filename):
    with open(filename) as f:
        version = None
        text = []
        for line in f:
            line = line.rstrip()
            if is_potential_version_line(line):
                # use it
                if is_line_with_version(line):
                    if version is not None:
                        yield version, text
                        version = None
                        text = []
                    version = normalize_version(line)
                else:
                    raise Exception("Unknown line: %s" % (line,))
            else:
                text.append(line)
    if version is not None:
        yield version, text


SRCS_DIR = "srcs"
ARCHIVES_DIR = "pub-tmp/archives"


def is_tarball_filename(filename):
    if fnmatch.fnmatch(filename, 'live.????.??.??.tar.gz'):
        return True
    return fnmatch.fnmatch(filename, 'live.????.??.???.tar.gz')


def get_version_from_filename(filename):
    if fnmatch.fnmatch(filename, 'live.????.??.??.tar.gz'):
        return filename[5:5 + 10]
    if fnmatch.fnmatch(filename, 'live.????.??.???.tar.gz'):
        return filename[5:5 + 11]

    raise Exception("Filename '%s' is not a valid live555 tarball" % (filename,))


# Returns
# srcs_tarballs :: dict<src :: String, [filename :: String]>
def read_srcs_tarballs():
    srcs_tarballs = {}
    for src in os.listdir(SRCS_DIR):
        for filename in os.listdir(join(SRCS_DIR, src)):
            if filename in ("README.md", "files.md5", "changelog.txt"):
                pass
            elif is_tarball_filename(filename):
                try:
                    srcs_tarballs[src].append(filename)
                except KeyError:
                    # TODO set() is the better datastructure
                    srcs_tarballs[src] = [filename]
            else:
                print("Warning: Ignoring '%s'" % (filename,), file=sys.stderr)

    return srcs_tarballs


# Swap keys and values
# - values must be a list/set!
def reverse_dict(d):
    r = {}
    for key in d:
        for value in d[key]:
            try:
                r[value].append(key)
            except KeyError:
                r[value] = [key]
    return r


def check_tarballs_for_equality():
    import filecmp

    srcs_tarballs = read_srcs_tarballs()
    tarballs_srcs = reverse_dict(srcs_tarballs)

    at_least_one_error = False

    duplicates = [(tarball, srcs) for tarball, srcs in tarballs_srcs.items() if len(srcs) >= 2]

    for tarball, srcs in duplicates:
        file_a = join(SRCS_DIR, srcs[0], tarball)
        for src in srcs[1:]:
            file_b = join(SRCS_DIR, src, tarball)
            check = filecmp.cmp(file_a, file_b)
            if not check:
                print("ERROR: Tarballs '%s' are different" % (tarball,))
                at_least_one_error = True

    if at_least_one_error:
        return 1

    return 0


def check_tarballs_for_versions_in_changelog():
    # TODO combine with other function
    srcs_tarballs = read_srcs_tarballs()
    tarballs_srcs = reverse_dict(srcs_tarballs)
    versions_from_tarballs = set(tarballs_srcs.keys())

    changelog = parse_changelog("changelog.txt")
    versions_from_changelog = set("live." + version + ".tar.gz" for version, _ in changelog)

    should_be_empty = versions_from_tarballs - versions_from_changelog
    if len(should_be_empty) != 0:
        print("ERROR: Some versions from tarballs are not in the changelog:", should_be_empty)
        return 1

    return 0


PREFER_UNIHAMBURG = {
    "live.2024.02.15.tar.gz", "live.2024.02.23.tar.gz",
    "live.2024.02.28.tar.gz", "live.2024.04.14.tar.gz",
    "live.2024.04.19.tar.gz", "live.2024.05.05.tar.gz",
    "live.2024.05.15.tar.gz", "live.2017.04.10.tar.gz",
    "live.2019.03.06.tar.gz", "live.2019.08.28.tar.gz"}


def choose_preferred_src(tarball, srcs):
    # Special case until 2024-06-15 before 'local2024' was introduced!
    if tarball in PREFER_UNIHAMBURG:
        assert "uni-hamburg.de" in srcs
        return "uni-hamburg.de"

    # And other special case. Otherwise 'localgetter' cannot be the preferred
    # src.
    if tarball == "live.2024.03.08.tar.gz":
        assert "jog.id.distfiles.macports.org" in srcs
        return "jog.id.distfiles.macports.org"

    if "localgetter" in srcs:
        return "localgetter"

    # Yet another special case: prefer "uni-hamburg.de" always over "tor".
    # Otherwise 'tor' would overrule all old tarballs.
    if "uni-hamburg.de" in srcs and "tor" in srcs:
        # But also use "jog.id.distfiles.macports.org" if there
        if "jog.id.distfiles.macports.org" in srcs:
            return "jog.id.distfiles.macports.org"
        # ... this function/approach does not scale ;-)
        if "local2023" in srcs:
            return "local2023"
        if "gentoo" in srcs:
            return "gentoo"
        return "uni-hamburg.de"

    # The default was to use the first one of the sorted list.
    return sorted(srcs)[0]


# tarballs_srcs :: dict<tarball :: string , [src :: string]>
# TODO make naming convention consistent!
def link_tarballs():
    srcs_tarballs = read_srcs_tarballs()
    tarballs_srcs = reverse_dict(srcs_tarballs)

    for tarball, srcs in tarballs_srcs.items():
        # Assumption: All tarballs are equal
        src = choose_preferred_src(tarball, srcs)

        link_target = join("..", "..", "srcs", src, tarball)
        link_path = join(ARCHIVES_DIR, tarball)

        os.symlink(link_target, link_path)

    return 0


def get_checksum_for_tarball(tarball_filename, checksum_file):
    with open(checksum_file) as f:
        for line in f:
            checksum, filename = line.rstrip("\n").split("  ", 1)
            if filename == tarball_filename:
                return checksum
    raise Exception("Checksum for tarball %s not found" % (tarball_filename,))


class PageType(Enum):
    LIST = "list"
    TABLE = "table"


def print_entry_for_tarball(page_type, version, tarball_filename, srcs, text):
    src = choose_preferred_src(tarball_filename, srcs)
    tarball_link = "https://github.com/lengfeld/live555-unofficial-archive/raw/main/srcs/%s/%s" % (src, tarball_filename)
    git_tag_name = "v%s-tree" % (version,)
    git_tag_link = "https://github.com/lengfeld/live555-unofficial-git-archive/tree/%s" % (git_tag_name,)
    tarball_size = os.path.getsize("pub-tmp/archives/" + tarball_filename)
    md5sum = get_checksum_for_tarball(tarball_filename, "pub-tmp/archives/checksums.md5")
    sha256sum = get_checksum_for_tarball(tarball_filename, "pub-tmp/archives/checksums.sha256")
    sha512sum = get_checksum_for_tarball(tarball_filename, "pub-tmp/archives/checksums.sha512")

    if page_type == PageType.LIST:
        print("<h2 id='%s'>%s</h2>" % (version, version))
        print("<ul>")
        print("<li>size: %d K</li>" % (tarball_size / 1024,))
        print("<li>tarball: <a href='%s'>%s</a></li>" % (tarball_link, tarball_filename))
        print("<li>git tag link: <a href='%s'>%s</a></li>" % (git_tag_link, git_tag_name))
        print("</ul>")
        # TODO add link to "git diff tag1..tag2"
        # TODO add link to patch file

        print("<h3>Changelog</h3>")
        print("<pre>%s</pre>" % ("\n".join(text),))

        print("<h3>Checksums</h3>")
        print("<ul>")
        print("<li>md5: %s</li>" % (md5sum,))
        print("<li>sha256: %s</li>" % (sha256sum,))
        print("<li>sha512: %s</li>" % (sha512sum,))
        print("</ul>")
    elif page_type == PageType.TABLE:
        print("<tr>")
        print("<td>%s</td>" % (version,))
        print("<td><a href='%s'>%s</a></td>" % (tarball_link, tarball_filename))
        print("<td><a href='%s'>%s</a></td>" % (git_tag_link, git_tag_name))
        print("<td>%d K</td>" % (tarball_size / 1024,))
        print("<td><a href='list.html#%s'>more</a></td>" % (version,))
        print("</tr>")
    else:
        assert(False)


def gen_list_or_table(page_type):
    srcs_tarballs = read_srcs_tarballs()
    tarballs_srcs = reverse_dict(srcs_tarballs)

    changelog = parse_changelog("changelog.txt")

    type
    print("<!doctype html>")
    print("<html lang='en-US'>")
    print("<head>")
    print("<meta charset='utf-8' />")
    print("<title>live555 unofficial archive - %s</title>" % (page_type.value,))
    print("</head>")
    print("<body>")
    print("<h1>live555 unofficial archive - %s</h1>" % (page_type.value,))

    if page_type == PageType.TABLE:
        print("<table>")
        print("<tr>")
        print("<th>filename</th>")
        print("<th>tarball</th>")
        print("<th>git tag</th>")
        print("<th>size</th>")
        print("<th>more information</th>")
        print("</tr>")


    for version, text in changelog:
        tarball = "live." + version + ".tar.gz"
        if tarball in tarballs_srcs:
            srcs = tarballs_srcs[tarball]
            print_entry_for_tarball(page_type, version, tarball, srcs, text)

    if page_type == PageType.TABLE:
        print("</table>")

    print("</body>")
    print("</html>")

    return 0


def create_git_tags():
    srcs_tarballs = read_srcs_tarballs()
    tarballs_srcs = reverse_dict(srcs_tarballs)

    for tarball in sorted(tarballs_srcs):
        srcs = tarballs_srcs[tarball]
        # Assumption: All tarballs are equal
        src = choose_preferred_src(tarball, srcs)

        version = get_version_from_filename(tarball)

        p = run(["scripts/unpack.sh", version, src])
        if p.returncode != 0:
            raise Exception("Command failed")

    return 0


def versions():
    for version, _ in parse_changelog("changelog.txt"):
        print(version)

    return 0


# TODO Enable this code
def unused_code():
    only_versions = False
    if "--versions" in sys.argv:
        only_versions = True

    for version, text in parse_changelog(filename):
        if only_versions:
            print(version)
        else:
            print(version, text)

    return 0


def main():
    if len(sys.argv) < 1:
        print("Usage: tdb")
        return 1

    cmd = sys.argv[1]

    if cmd == "check":
        ret = check_tarballs_for_equality()
        if ret != 0:
            return ret
        return check_tarballs_for_versions_in_changelog()
    elif cmd == "link":
        return link_tarballs()
    elif cmd == "tag":
        return create_git_tags()
    elif cmd == "list":
        return gen_list_or_table(PageType.LIST)
    elif cmd == "table":
        return gen_list_or_table(PageType.TABLE)
    elif cmd == "versions":
        return versions()
    else:
        print("ERROR: Unknown cmd '%s'" % (cmd,))
        return 1


if __name__ == '__main__':
    sys.exit(main())
