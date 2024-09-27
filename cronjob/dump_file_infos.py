#!/usr/bin/env python3

import sys
from parse_html import parse_html
from parse_table_data import parse_table_data


def main():
    filenames = sys.argv[1:]

    if len(filenames) < 1:
        print("Error: No filename is provied!", file=sys.stderr)
        return 1

    for filename in filenames:
        with open(filename) as f:
            html = f.read()

        table_data = parse_html(html)
        file_infos = parse_table_data(table_data)
        for file_info in file_infos:
            print(file_info)

    return 0


if __name__ == "__main__":
    sys.exit(main())
