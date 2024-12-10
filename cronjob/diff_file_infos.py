#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2024 Stefan Lengfeld <stefan@lengfeld.xyz>

import sys
import unittest
from parse_html import parse_html
from parse_table_data import parse_table_data, FileInfo
from collections import namedtuple
from enum import Enum, auto


class Changes(Enum):
    NEW = 'N'
    DELETED = 'D'
    MODIFIED = 'M'


def diff_file_infos(file_infos_a, file_infos_b):
    file_infos_a.sort(key=lambda file_info: file_info.name)
    file_infos_b.sort(key=lambda file_info: file_info.name)

    pos_a = 0
    pos_b = 0
    diff = []
    while True:
        if pos_a >= len(file_infos_a):
            # List A is finished
            # everything in B is new
            for i in range(pos_b, len(file_infos_b)):
                diff.append((Changes.NEW, file_infos_b[i].name))
            break
        if pos_b >= len(file_infos_b):
            # List B is finished
            # everything in A is removed
            for i in range(pos_a, len(file_infos_a)):
                diff.append((Changes.DELETED, file_infos_a[i].name))
            break

        # Compare the name
        name_a = file_infos_a[pos_a].name
        name_b = file_infos_b[pos_b].name
        if name_a < name_b:
            # The file in A is not anymore in the list B. So it was removed!
            diff.append((Changes.DELETED, name_a))
            pos_a += 1
        elif name_a > name_b:
            # The file in B is not in the list A. So it's new!
            diff.append((Changes.NEW, name_b))
            pos_b += 1
        else:
            assert(name_a == name_b)
            # A and B have the same name. Are they the same?
            if file_infos_a[pos_a] == file_infos_b[pos_b]:
                # Yes the are the same. So there is _no_ diff!
                pass
            else:
                # They are different!
                diff.append((Changes.MODIFIED, name_b))
            pos_a += 1
            pos_b += 1

    return diff


def MyFileInfo(name, lastModified=''):
    return FileInfo(name=name, lastModified=lastModified, size='', description='')


class TestDiffFileInfos(unittest.TestCase):
    def testNothing(self):
        file_infos_a = []
        file_infos_b = []
        diff = diff_file_infos(file_infos_a, file_infos_b)
        self.assertEqual(diff, [])

    def testOneFileNew(self):
        file_infos_a = []
        file_infos_b = [MyFileInfo('filename')]
        diff = diff_file_infos(file_infos_a, file_infos_b)
        self.assertEqual(diff, [(Changes.NEW, 'filename')])

    def testOneFileRemoved(self):
        file_infos_a = [MyFileInfo('filename')]
        file_infos_b = []
        diff = diff_file_infos(file_infos_a, file_infos_b)
        self.assertEqual(diff, [(Changes.DELETED, 'filename')])

    def testOneFileModified(self):
        file_infos_a = [MyFileInfo('filename', lastModified='1')]
        file_infos_b = [MyFileInfo('filename', lastModified='2')]
        diff = diff_file_infos(file_infos_a, file_infos_b)
        self.assertEqual(diff, [(Changes.MODIFIED, 'filename')])

    def testOneFileNotModified(self):
        file_infos_a = [MyFileInfo('filename', lastModified='1')]
        file_infos_b = [MyFileInfo('filename', lastModified='1')]
        diff = diff_file_infos(file_infos_a, file_infos_b)
        self.assertEqual(diff, [])

    def testRemovedInMultipleFiles(self):
        file_infos_a = [MyFileInfo('a'), MyFileInfo('b'), MyFileInfo('c')]
        file_infos_b = [MyFileInfo('a'), MyFileInfo('c')]
        diff = diff_file_infos(file_infos_a, file_infos_b)
        self.assertEqual(diff, [(Changes.DELETED, 'b')])

    def testNewInMultipleFiles(self):
        file_infos_a = [MyFileInfo('a'), MyFileInfo('c')]
        file_infos_b = [MyFileInfo('a'), MyFileInfo('b'), MyFileInfo('c')]
        diff = diff_file_infos(file_infos_a, file_infos_b)
        self.assertEqual(diff, [(Changes.NEW, 'b')])

    def testNotModifiedInMultipleFiles(self):
        file_infos_a = [MyFileInfo('a'), MyFileInfo('b', lastModified='1'), MyFileInfo('c')]
        file_infos_b = [MyFileInfo('a'), MyFileInfo('b', lastModified='1'), MyFileInfo('c')]
        diff = diff_file_infos(file_infos_a, file_infos_b)
        self.assertEqual(diff, [])

    def testModifiedInMultipleFiles(self):
        file_infos_a = [MyFileInfo('a'), MyFileInfo('b', lastModified='1'), MyFileInfo('c')]
        file_infos_b = [MyFileInfo('a'), MyFileInfo('b', lastModified='2'), MyFileInfo('c')]
        diff = diff_file_infos(file_infos_a, file_infos_b)
        self.assertEqual(diff, [(Changes.MODIFIED, 'b')])


def read_and_parse_file(filename):
    with open(filename) as f:
        html = f.read()
        table_data = parse_html(html)
        file_infos = parse_table_data(table_data)
        return file_infos


# TODO Having this in the same file as the function 'diff_file_infos' is not so nice.
# I a have to import all other functoins that do parsing on 'html' and 'table_data'
def main():
    filenames = sys.argv[1:]

    if len(filenames) != 2:
        print("Error: Give two files!", file=sys.stderr)
        return 1

    file_infos_a = read_and_parse_file(filenames[0])
    file_infos_b = read_and_parse_file(filenames[1])

    diff = diff_file_infos(file_infos_a, file_infos_b)
    for change, filename in diff:
        print(change.value, filename)

    return 0


import subprocess
from subprocess import DEVNULL, PIPE


class TestDiffFileInfosProgram(unittest.TestCase):
    def testErrorNoFilename(self):
        p = subprocess.run(["./diff_file_infos.py"], stderr=DEVNULL)
        self.assertEqual(p.returncode, 1)

    def testErrorFilesNotFound(self):
        p = subprocess.run(["./diff_file_infos.py", "not found", "not found2"], stderr=DEVNULL)
        self.assertEqual(p.returncode, 1)

    def testDiffWithoutChanges(self):
        # TODO Do not use external files. Have a context wrapper to create a file with a specifc content!
        p = subprocess.run(["./diff_file_infos.py", "content-example.html", "content-example.html"], stdout=PIPE)
        self.assertEqual(p.returncode, 0)
        self.assertEqual(p.stdout, b"")

    def testDiffWithoutChanges(self):
        p = subprocess.run(["./diff_file_infos.py", "content-example.html", "content-example.2.html"], stdout=PIPE)
        self.assertEqual(p.returncode, 0)
        self.assertEqual(p.stdout,b"""M changelog.txt
M doxygen/
D live.2023.03.30.tar.gz
N live.2023.07.24.tar.gz
M live555-latest-sha1.txt
M live555-latest.tar.gz
""")


if __name__ == "__main__":
    sys.exit(main())
