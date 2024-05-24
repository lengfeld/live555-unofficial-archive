#!/usr/bin/env python3

import os
import sys
import fnmatch
from os.path import join

# NOTE: All paths are hardcoded. It must be executed in the top level driectory
# of the repo.


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
    # Normale cases
    if fnmatch.fnmatch(line, '????.??.??:'):
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


def normalize_version(line):
    line = line.rstrip(":")
    line = line.replace("-", ".")
    if line == "2003:03;11":
        line = "2003.03.11"
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


def read_tarballs():
    tarballs = {}
    for src in os.listdir(SRCS_DIR):
        for file in os.listdir(join(SRCS_DIR, src)):
            if file in ("README.md", "files.md5", "changelog.txt"):
                pass
            elif fnmatch.fnmatch(file, 'live.????.??.??.tar.gz') or fnmatch.fnmatch(file, 'live.????.??.???.tar.gz'):
                try:
                    tarballs[src].append(file)
                except KeyError:
                    # TODO set() is the better datastructure
                    tarballs[src] = [file]
            else:
                print("Warning: Ignoring '%s'" % (file,))

    return tarballs


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

    srcs_with_tarballs = read_tarballs()
    tarballs = reverse_dict(srcs_with_tarballs)

    at_least_one_error = False

    duplicates = [tarball for tarball, srcs in tarballs.items() if len(srcs) >= 2]

    for duplicate in duplicates:
        srcs = tarballs[duplicate]
        file_a = join(SRCS_DIR, srcs[0], duplicate)
        for src in srcs[1:]:
            file_b = join(SRCS_DIR, src, duplicate)
            check = filecmp.cmp(file_a, file_b)
            if not check:
                print("ERROR: Tarballs '%s' are different" % (duplicate,))
                at_least_one_error = True

    if at_least_one_error:
        return 1

    return 0


def check_tarballs_for_versions_in_changelog():
    # TODO combine with other function
    srcs_with_tarballs = read_tarballs()
    tarballs = reverse_dict(srcs_with_tarballs)

    changelog = list(parse_changelog("changelog.txt"))
    versions_from_tarballs = set(tarballs.keys())
    versions_from_changelog = set("live." + version + ".tar.gz" for version, _ in changelog)

    should_be_empty = versions_from_tarballs - versions_from_changelog
    if len(should_be_empty) != 0:
        print("ERROR: Some versions from tarballs are not in the changelog:", should_be_empty)
        return 1

    return 0


# tarballs :: dict<filename, srcs>
# TODO make naming convention consistent!
def link_tarballs():
    srcs_with_tarballs = read_tarballs()
    tarballs = reverse_dict(srcs_with_tarballs)

    for filename, srcs in tarballs.items():
        # Just pick the first one. Assumption: All tarballs are equal
        # Use "sorted" to make the selection consistent
        src = sorted(srcs)[0]

        link_target = join("..", "..", "srcs", src, filename)
        link_path = join("archives", "all", filename)

        os.symlink(link_target, link_path)

    return 0


# TODO Renable this code
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
    else:
        print("ERROR: Unknown cmd '%s'" % (cmd,))
        return 1


if __name__ == '__main__':
    sys.exit(main())
