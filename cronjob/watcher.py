#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2024 Stefan Lengfeld <stefan@lengfeld.xyz>

import sys
from localwebserver import LocalWebserver
import unittest
import requests
from subprocess import run, PIPE

from http.server import SimpleHTTPRequestHandler
from parse_html import parse_html
from parse_table_data import parse_table_data, FileInfo

from diff_file_infos import diff_file_infos, Changes


def read_state_as_file_infos():
    with open("state", "r") as f:
        html = f.read()
        table_data = parse_html(html)
        return parse_table_data(table_data)


def dump():
    try:
        file_infos = read_state_as_file_infos()
        for file_info in file_infos:
            print(file_info)
    except FileNotFoundError:
        print("ERROR: No state available", file=sys.stderr)
        return 1

    return 0

def get_remote(url):
    r = requests.get(url)
    if r.status_code != 200:
        raise Exception("Request failed %s" % (r,))
    if not "text/html" in r.headers["content-type"]:
        raise Exception("Wrong content-type: %s " % (r.headers["content-type"],))

    remote_html = r.text
    remote_as_file_infos = parse_table_data(parse_html(remote_html))

    return remote_html, remote_as_file_infos


def diff(url):
    # TODO check for file not found!
    state_as_file_infos = read_state_as_file_infos()

    _, remote_as_file_infos = get_remote(url)

    diff = diff_file_infos(state_as_file_infos, remote_as_file_infos)
    for change, filename in diff:
        print(change.value, filename)

    return 0

def get_iso_utc_string():
    import time
    return time.strftime("%Y-%m-%dT%H:%M:%S%z", time.gmtime())

def get(url):
    # DO this at the beginning to get the start time of the query.

    dir_name = get_iso_utc_string()

    state_as_file_infos = read_state_as_file_infos()

    remote_html, remote_as_file_infos = get_remote(url)

    diff = diff_file_infos(state_as_file_infos, remote_as_file_infos)

    # What are the new and modified files?
    changed_files = []
    for change, filename in diff:
        if change in (Changes.NEW, Changes.MODIFIED):
            changed_files.append(filename)

    if len(changed_files) == 0:
        # Nothing do it. No files were changed
        return 0

    def get_file_info_for_filename(filename):
        for file_info in remote_as_file_infos:
            if file_info.name == filename:
                return file_info
        raise ValueError("Filename not found")

    print("Changed files:")
    # TODO maybe add flag. Maybe add info of old file!
    # TODO use the same output as 'diff'
    for filename in changed_files:
        print(get_file_info_for_filename(filename))

    IGNORE_FILES = ["doxygen/"]

    # Filter out some files
    changed_files = [n for n in changed_files if n not in IGNORE_FILES]

    os.mkdir(dir_name)
    print("Creating and using dir: %s" % (dir_name,))
    with cwd(dir_name):
        # For now, just use wget instead of python code
        for filename in changed_files:
            # Now download every new file
            file_url = url + filename
            print("Downloading %s" % (file_url,))
            p = run(["wget", "--quiet", file_url])
            if p.returncode != 0:
                raise Exception("Wget failed: %d" % (p.returncode,))

        # Also save the retreived html in the folder for later inspection
        with open("index.html", "w") as f:
            f.write(remote_html)

    # Update state file with new html
    # TODO make this atomic
    with open("state", "w") as f:
        f.write(remote_html)

    return 0


def main():
    if len(sys.argv) != 3:
        print("Usage: %s <cmd> <url>" % (sys.argv[0],), file=sys.stderr)
        print("cmds: 'dump', 'diff', 'get'", file=sys.stderr)
        return 1

    cmd = sys.argv[1]
    url = sys.argv[2]

    if cmd not in ("dump", "diff", "get"):
        print("Error: invalid cmd", file=sys.stderr)
        return 1

    if cmd == "dump":
        return dump()
    elif cmd == "diff":
        return diff(url)
    elif cmd == "get":
        return get(url)
    else:
        raise Exception("Never reached")


import os
import tempfile
import shutil
import contextlib
from os.path import isfile, isdir, join, realpath, dirname


@contextlib.contextmanager
def mktmpdir():
    tmpdir = tempfile.mkdtemp(prefix="tmpdir-", dir=os.path.dirname(__file__))
    try:
        yield tmpdir
    finally:
        shutil.rmtree(tmpdir)


@contextlib.contextmanager
def cwd(cwd):
    old_cwd = os.getcwd()
    try:
        os.chdir(cwd)
        yield
    finally:
        os.chdir(old_cwd)



class HandlerMy(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open("content-example.html", "rb") as f:
                self.wfile.write(f.read())
        else:
            self.send_response(404)
            self.end_headers()




class TestXXX(unittest.TestCase):
    def testNoArgs(self):
        p = run(["./watcher.py"], stdout=PIPE, stderr=PIPE)
        self.assertEqual(1, p.returncode)
        self.assertEqual(p.stdout, b"")
        self.assertEqual(p.stderr,
b"""Usage: ./watcher.py <cmd> <url>
cmds: 'dump', 'diff', 'get'
""")

    def testDumpNostate(self):
        with mktmpdir() as tmpdir, cwd(tmpdir):
            p = run(["../watcher.py", "dump", "http://[::1]:8000/"], stdout=PIPE, stderr=PIPE)
            self.assertEqual(1, p.returncode)
            self.assertEqual(p.stdout, b"")
            self.assertEqual(p.stderr, b"ERROR: No state available\n")

    def testDump(self):
        with mktmpdir() as tmpdir, cwd(tmpdir):
            shutil.copyfile("../content-example.html", join(tmpdir, "state"))
            p = run(["../watcher.py", "dump", "http://[::1]:8000/"], stdout=PIPE)
            self.assertEqual(0, p.returncode)
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

    def diffAndGetStdout(self, state_filename, remote_filename):
        class HandlerMy(SimpleHTTPRequestHandler):
            def do_GET(self):
                if self.path == '/':
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    with open(remote_filename, "rb") as f:
                        self.wfile.write(f.read())
                else:
                    self.send_response(404)
                    self.end_headers()

        with mktmpdir() as tmpdir, cwd(tmpdir), LocalWebserver(8000, HandlerMy):
            shutil.copyfile(state_filename, join(tmpdir, "state"))
            p = run(["../watcher.py", "diff", "http://[::1]:8000/"], stdout=PIPE)
            self.assertEqual(0, p.returncode)
            return p.stdout

    # TODO Test 404 from server
    def testDiffEmpty(self):
        stdout = self.diffAndGetStdout("../content-example.html", "../content-example.html")
        self.assertEqual(stdout, b"")

    def testDiffWithChangesFiles(self):
        stdout = self.diffAndGetStdout("../content-example.html", "../content-example.2.html")
        self.assertEqual(stdout,
b"""M changelog.txt
M doxygen/
D live.2023.03.30.tar.gz
N live.2023.07.24.tar.gz
M live555-latest-sha1.txt
M live555-latest.tar.gz
""")

    def testGetNoChanges(self):
        class HandlerMy(SimpleHTTPRequestHandler):
            def do_GET(self):
                if self.path == '/':
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    with open("../content-example.html", "rb") as f:
                        self.wfile.write(f.read())
                else:
                    self.send_response(404)
                    self.end_headers()

        with mktmpdir() as tmpdir, cwd(tmpdir), LocalWebserver(8000, HandlerMy):
            shutil.copyfile("../content-example.html", join(tmpdir, "state"))
            p = run(["../watcher.py", "get", "http://[::1]:8000/"], stdout=PIPE)
            self.assertEqual(0, p.returncode)
            self.assertEqual(p.stdout, b"")

    def assertFile(self, filename, expected):
        with open(filename, "br") as f:
            actual = f.read()
            self.assertEqual(expected, actual)

    def testGetChanges(self):
        FILES = {"/changelog.txt": b"xyz01",
                 "/live.2023.07.24.tar.gz": b"xyz02",
                 "/live555-latest-sha1.txt": b"xyz03",
                 "/live555-latest.tar.gz": b"xyz04"}

        class HandlerMy(SimpleHTTPRequestHandler):
            def do_GET(self):
                if self.path == '/':
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    with open("../content-example.2.html", "rb") as f:
                        self.wfile.write(f.read())
                elif self.path in FILES:
                    # The local server must also serve the changed files for
                    # the test
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(FILES[self.path])
                else:
                    self.send_response(404)
                    self.end_headers()

        with mktmpdir() as tmpdir, cwd(tmpdir), LocalWebserver(8000, HandlerMy):
            shutil.copyfile("../content-example.html", join(tmpdir, "state"))
            p = run(["../watcher.py", "get", "http://[::1]:8000/"], stdout=PIPE)
            self.assertEqual(0, p.returncode)

            # get filename
            dirname = [name for name in os.listdir() if name != "state"][0]
            self.assertTrue(os.path.isdir(dirname))

            self.assertEqual(p.stdout,
b"""Changed files:
FileInfo(name='changelog.txt', lastModified='2023-07-24 16:20', size='365K', description='')
FileInfo(name='doxygen/', lastModified='2023-07-24 16:21', size='-', description='')
FileInfo(name='live.2023.07.24.tar.gz', lastModified='2023-07-24 16:20', size='673K', description='')
FileInfo(name='live555-latest-sha1.txt', lastModified='2023-07-24 16:20', size='41', description='')
FileInfo(name='live555-latest.tar.gz', lastModified='2023-07-24 16:20', size='673K', description='')
Creating and using dir: %s
Downloading http://[::1]:8000/changelog.txt
Downloading http://[::1]:8000/live.2023.07.24.tar.gz
Downloading http://[::1]:8000/live555-latest-sha1.txt
Downloading http://[::1]:8000/live555-latest.tar.gz
""" % (dirname.encode("ascii"),))

            self.assertFile(join(dirname, "changelog.txt"), b"xyz01")
            self.assertFile(join(dirname, "live.2023.07.24.tar.gz"), b"xyz02")
            self.assertFile(join(dirname, "live555-latest-sha1.txt"), b"xyz03")
            self.assertFile(join(dirname, "live555-latest.tar.gz"), b"xyz04")
            with open("../content-example.2.html", "br") as f:
                content_example_new = f.read()
            self.assertFile(join(dirname, "index.html"), content_example_new)

            # Now run again. The watcher should update the state file and no further download should happen
            p = run(["../watcher.py", "get", "http://[::1]:8000/"], stdout=PIPE)
            self.assertEqual(p.returncode, 0)
            self.assertEqual(p.stdout, b"")


if __name__ == "__main__":
    sys.exit(main())
