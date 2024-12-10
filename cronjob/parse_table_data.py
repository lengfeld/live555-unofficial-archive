#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2024 Stefan Lengfeld <stefan@lengfeld.xyz>

import unittest
from parse_html import TableData
from collections import namedtuple
from enum import Enum, auto


class ConvertErrorReason(Enum):
    TITLE_DOES_NOT_MATCH = auto()
    TABLE_HEADERS_DO_NOT_MATCH = auto()


class ConvertError(Exception):
    def __init__(self, reason):
        self.reason = reason


# TODO rename 'name' to 'filename'. IN other code I now used the word 'filename'
FileInfo = namedtuple('FileInfo', 'name lastModified size description')

# Html :: String
# TableData :: title, rows, headers
# FileInfos :: List<FileInfo>
def parse_table_data(table_data):
    if table_data.title != "Index of /liveMedia/public":
        raise ConvertError(ConvertErrorReason.TITLE_DOES_NOT_MATCH)

    # NOTE: The last two empty header cells are not in the frist row.
    if table_data.headers != ['', 'Name', 'Last modified', 'Size', 'Description', '', '']:
        raise ConvertError(ConvertErrorReason.TABLE_HEADERS_DO_NOT_MATCH)

    file_infos = []
    for row in table_data.rows:
        name = row[1].strip()
        # Apply strip() to remove trailling whitespaces
        file_info = FileInfo(name, row[2].strip(), row[3].strip(), row[4].strip())
        file_infos.append(file_info)

    return file_infos


class TestParseTableData(unittest.TestCase):
    def testTitleIsWrong(self):
        table_data = TableData("Index of /wrong", [], [])
        with self.assertRaises(ConvertError) as context:
                parse_table_data(table_data)
        self.assertEqual(context.exception.reason, ConvertErrorReason.TITLE_DOES_NOT_MATCH)

    def testTableHeadersToNotMatch(self):
        table_data = TableData("Index of /liveMedia/public", ["", "Name", "Last modified", "Size", "WRONG", "", ""], [])
        with self.assertRaises(ConvertError) as context:
                parse_table_data(table_data)
        self.assertEqual(context.exception.reason, ConvertErrorReason.TABLE_HEADERS_DO_NOT_MATCH)

    def testOneFileInfo(self):
        rows = [["", "live555-latest-sha1.txt", "2023-03-30 08:47", "41", ""]]
        table_data = TableData("Index of /liveMedia/public", ["", "Name", "Last modified", "Size", "Description", "", ""], rows)
        file_infos = parse_table_data(table_data)
        self.assertEqual(file_infos, [FileInfo(name='live555-latest-sha1.txt', lastModified='2023-03-30 08:47', size='41', description='')])


if __name__ == "__main__":
    unittest.main()
