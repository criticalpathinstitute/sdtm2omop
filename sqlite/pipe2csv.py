#!/usr/bin/env python3
"""
Author : Ken Youens-Clark <kyclark@gmail.com>
Date   : 2021-09-09
Purpose: Rock the Casbah
"""

import argparse
import csv
from typing import NamedTuple, TextIO


class Args(NamedTuple):
    """ Command-line arguments """
    in_file: TextIO
    out_file: TextIO


# --------------------------------------------------
def get_args() -> Args:
    """ Get command-line arguments """

    parser = argparse.ArgumentParser(
        description='Rock the Casbah',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('in_file',
                        help='Input pipe-delimited file',
                        metavar='FILE',
                        type=argparse.FileType('rt'))

    parser.add_argument('out_file',
                        help='Output comma-delimited file',
                        metavar='FILE',
                        type=argparse.FileType('wt'))

    args = parser.parse_args()

    return Args(args.in_file, args.out_file)


# --------------------------------------------------
def main() -> None:
    """ Make a jazz noise here """

    args = get_args()
    fields = [
        'cui', 'language', 'term_status', 'lui', 'string_type', 'sui',
        'atom_status', 'aui', 'saui', 'scui', 'sdui', 'source_name',
        'term_type', 'code', 'string', 'srl', 'suppress', 'cvf'
    ]

    writer = csv.DictWriter(args.out_file, fieldnames=fields, delimiter=',')
    writer.writeheader()

    for i, line in enumerate(args.in_file, start=1):
        print(f'{i:9}')
        writer.writerow(dict(zip(fields, line.split('|'))))

    print('Done')


# --------------------------------------------------
if __name__ == '__main__':
    main()
