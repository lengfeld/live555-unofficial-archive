#!/usr/bin/python3

import unittest
from html.parser import HTMLParser
from collections import namedtuple
from enum import Enum, auto


TableData = namedtuple('TableData', 'title headers rows')


class State(Enum):
    NONE = auto()
    # NOTE: Title is a special case. Code can be more generic.
    IN_TITLE = auto()
    IN_TABLE = auto()
    IN_TABLE_TR = auto()
    IN_TABLE_TR_TH = auto()
    IN_TABLE_TR_TD = auto()


class ParseError(Exception):
    pass


# See https://docs.python.org/3.9/library/html.parser.html
class MyHtmlParser(HTMLParser):
    def __init__(self):
        self._title = None
        self._state = State.NONE
        self._headers = []
        self._rows = []
        self._current_row = []
        self._current_cell = None
        super().__init__()

    def handle_starttag(self, tag, attrs):
        if tag == "title":
            if self._state != State.NONE:
                raise ParseError()
            self._state = State.IN_TITLE
        elif tag == "table":
            if self._state != State.NONE:
                raise ParseError()
            self._state = State.IN_TABLE
        elif tag == "tr":
            if self._state != State.IN_TABLE:
                raise ParseError()
            self._state = State.IN_TABLE_TR
        elif tag == "th":
            if self._state != State.IN_TABLE_TR:
                raise ParseError()
            self._state = State.IN_TABLE_TR_TH
            if self._current_cell is not None:
                raise ParseError()
            self._current_cell = ""
        elif tag == "td":
            if self._state != State.IN_TABLE_TR:
                raise ParseError()
            self._state = State.IN_TABLE_TR_TD
            if self._current_cell is not None:
                raise ParseError()
            self._current_cell = ""

    def handle_endtag(self, tag):
        if tag == "title":
            if self._state != State.IN_TITLE:
                raise ParseError()
            self._state = State.NONE
        elif tag == "table":
            if self._state != State.IN_TABLE:
                raise ParseError()
            self._state = State.NONE
        elif tag == "tr":
            if self._state != State.IN_TABLE_TR:
                raise ParseError()
            self._state = State.IN_TABLE
            # Special here: finalize current row
            if len(self._current_row) != 0:
                self._rows.append(self._current_row)
                self._current_row = []
        elif tag == "th":
            if self._state != State.IN_TABLE_TR_TH:
                raise ParseError()
            # End of <th> reached. Finalize cell.
            self._headers.append(self._current_cell)
            self._current_cell = None
            self._state = State.IN_TABLE_TR
        elif tag == "td":
            if self._state != State.IN_TABLE_TR_TD:
                raise ParseError()
            # End of <td> reached. Finalize cell.
            self._current_row.append(self._current_cell)
            self._current_cell = None
            self._state = State.IN_TABLE_TR

    def handle_data(self, data):
        if self._state == State.IN_TITLE:
            self._title = data
        elif self._state == State.IN_TABLE_TR_TH:
            if self._current_cell is None:
                raise ParseError()
            self._current_cell += data
        elif self._state == State.IN_TABLE_TR_TD:
            # If a <td> contains html elements, concat every data in those
            # elements. Example:
            #    <td><a href="264/">264/</a> y </td>
            # becomes
            #    "264 y "
            if self._current_cell is None:
                raise ParseError()
            self._current_cell += data

    def get_result(self):
        return TableData(self._title, self._headers, self._rows)


def parse_html(html):
    parser = MyHtmlParser()
    parser.feed(html)
    return parser.get_result()


class TestParseHtml(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open("content-example.html") as f:
            cls.content_example = f.read()

    def testParseRealWorldData(self):
        table_data = parse_html(self.content_example)
        self.assertEqual("Index of /liveMedia/public", table_data.title)
        # NOTE: The last two header titles are not in the first row.
        # They are in the second row
        #    <tr><th colspan="5"><hr></th></tr>
        # And in the last row!
        # TODO Improve parser to parse 'th' elements in multiple rows
        # correctly.
        self.assertEqual(table_data.headers, ['', 'Name', 'Last modified', 'Size', 'Description', '', ''])
        # TODO Add more checks
        #print(table_data.headers)
        #for row in table_data.rows:
        #    print(row)

    def testTitle(self):
        table_data = parse_html("<html><head><title>Index of /liveMedia/public</title></head></html>")
        self.assertEqual(table_data.title, "Index of /liveMedia/public")

    def testTableEmpty(self):
        table_data = parse_html("<table></table>")
        self.assertEqual(table_data.headers, [])
        self.assertEqual(table_data.rows, [])

    def testTableHeader(self):
        table_data = parse_html("<table><tr><th>hello</th><th>2</th></tr></table>")
        self.assertEqual(table_data.headers, ['hello', '2'])
        self.assertEqual(table_data.rows, [])

    def testTableRow(self):
        table_data = parse_html("<table><tr><td>hello</td><td>2</td></tr></table>")
        self.assertEqual(table_data.headers, [])
        self.assertEqual(table_data.rows, [['hello', '2']])

    def testTableRowTooShort(self):
        table_data = parse_html("<table><tr><td>hello</td><td>2</td></tr><tr><td>2x</td></tr></table>")
        self.assertEqual(table_data.headers, [])
        # Second row has only one instead of two elements
        self.assertEqual(table_data.rows, [['hello', '2'], ['2x']])

    def testCellContainsExtraHtmlElementAndTrialingWhitespace(self):
        table_data = parse_html("<table><tr><td><p>xxx</p>   </td><td>y</td></tr></table>")
        self.assertEqual(table_data.headers, [])
        self.assertEqual(table_data.rows, [['xxx   ', 'y']])

    def testTableHeaderCellWithoutContent(self):
        table_data = parse_html("<table><tr><th></th></tr></table>")
        self.assertEqual(table_data.headers, [''])
        self.assertEqual(table_data.rows, [])

    def testTableRowCellWithoutContent(self):
        table_data = parse_html("<table><tr><td></td></tr></table>")
        self.assertEqual(table_data.headers, [])
        self.assertEqual(table_data.rows, [['']])


if __name__ == "__main__":
    unittest.main()
