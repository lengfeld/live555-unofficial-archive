#!/usr/bin/env python3

import unittest
import subprocess
from subprocess import DEVNULL, PIPE


class TestDumpFileInfos(unittest.TestCase):
    def testErrorNoFilename(self):
        p = subprocess.run(["./dump_file_infos.py"], stderr=DEVNULL)
        self.assertEqual(p.returncode, 1)

    def testErrorFileNotFound(self):
        p = subprocess.run(["./dump_file_infos.py", "not found"], stderr=DEVNULL)
        self.assertEqual(p.returncode, 1)

    def testSuccess(self):
        p = subprocess.run(["./dump_file_infos.py", "content-example.html"], stdout=PIPE)
        self.assertEqual(p.returncode, 0)
        self.assertEqual(p.stdout,
b"""FileInfo(name='Parent Directory', lastModified='', size='-', description='')
FileInfo(name='264/', lastModified='2016-04-20 13:02', size='-', description='')
FileInfo(name='265/', lastModified='2014-03-03 12:19', size='-', description='')
FileInfo(name='aac/', lastModified='2011-03-05 21:35', size='-', description='')
FileInfo(name='changelog.txt', lastModified='2023-03-30 08:52', size='363K', description='')
FileInfo(name='doxygen/', lastModified='2023-03-30 08:47', size='-', description='')
FileInfo(name='favicon.ico', lastModified='2010-12-12 08:47', size='1.4K', description='')
FileInfo(name='h264-in-mp2t/', lastModified='2018-03-04 08:32', size='-', description='')
FileInfo(name='live-devel-archives-..>', lastModified='2005-07-14 07:19', size='6.5M', description='')
FileInfo(name='live.2023.03.30.tar.gz', lastModified='2023-03-30 08:47', size='711K', description='')
FileInfo(name='live555-latest-sha1.txt', lastModified='2023-03-30 08:47', size='41', description='')
FileInfo(name='live555-latest.tar.gz', lastModified='2023-03-30 08:47', size='711K', description='')
FileInfo(name='m4e/', lastModified='2007-08-08 00:30', size='-', description='')
FileInfo(name='opus/', lastModified='2014-11-12 05:56', size='-', description='')
""")
