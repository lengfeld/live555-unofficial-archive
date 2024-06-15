#!/usr/bin/env python3

import os
import sys
import fnmatch
from os.path import join
from subprocess import run

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
                print("Warning: Ignoring '%s'" % (filename,))

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

    changelog = list(parse_changelog("changelog.txt"))
    versions_from_changelog = set("live." + version + ".tar.gz" for version, _ in changelog)

    should_be_empty = versions_from_tarballs - versions_from_changelog
    if len(should_be_empty) != 0:
        print("ERROR: Some versions from tarballs are not in the changelog:", should_be_empty)
        return 1

    return 0


# tarballs_srcs :: dict<tarball :: string , [src :: string]>
# TODO make naming convention consistent!
def link_tarballs():
    srcs_tarballs = read_srcs_tarballs()
    tarballs_srcs = reverse_dict(srcs_tarballs)

    for tarball, srcs in tarballs_srcs.items():
        # Just pick the first one. Assumption: All tarballs are equal
        # Use "sorted" to make the selection consistent
        src = sorted(srcs)[0]

        link_target = join("..", "..", "srcs", src, tarball)
        link_path = join(ARCHIVES_DIR, tarball)

        os.symlink(link_target, link_path)

    return 0


def create_git_tags():
    srcs_tarballs = read_srcs_tarballs()
    tarballs_srcs = reverse_dict(srcs_tarballs)

    for tarball, srcs in tarballs_srcs.items():
        # Just pick the first one. Assumption: All tarballs are equal
        # Use "sorted" to make the selection consistent
        src = sorted(srcs)[0]

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
    elif cmd == "versions":
        return versions()
    else:
        print("ERROR: Unknown cmd '%s'" % (cmd,))
        return 1


if __name__ == '__main__':
    sys.exit(main())
