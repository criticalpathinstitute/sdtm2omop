#!/usr/bin/env python3
"""
Author : Ken Youens-Clark <kyclark@gmail.com>
Date   : 2021-09-08
Purpose: Load concepts into SQLite
"""

import argparse
import csv
import os
from typing import NamedTuple, TextIO
from pprint import pprint
from concepts import UmlsConcept, SnomedConcept


class Args(NamedTuple):
    """ Command-line arguments """
    file: TextIO
    db_name: str


# --------------------------------------------------
def get_args() -> Args:
    """ Get command-line arguments """

    parser = argparse.ArgumentParser(
        description='Load concepts into SQLite',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('file',
                        help='UMLS file',
                        metavar='FILE',
                        type=argparse.FileType('rt'))

    parser.add_argument('-d',
                        '--db',
                        help='SQLite database',
                        metavar='STR',
                        default='concepts.db')

    args = parser.parse_args()

    if not os.path.isfile(args.db):
        parser.error(f'Invalid --db "{args.db}"')

    return Args(args.file, args.db)


# --------------------------------------------------
def main() -> None:
    """ Make a jazz noise here """

    args = get_args()
    fields = [
        'cui', 'language', 'term_status', 'lui', 'string_type', 'sui',
        'atom_status', 'aui', 'saui', 'scui', 'sdui', 'source_name',
        'term_type', 'code', 'string', 'srl', 'suppress', 'cvf'
    ]

    # reader = csv.DictReader(args.file, fieldnames=fields, delimiter='|')
    for i, line in enumerate(args.file, start=1):
        rec = dict(zip(fields, line.split('|')))
        # pprint(rec)
        print(f"{i:9,}: {rec['code']}")
        concept, _ = UmlsConcept.get_or_create(**{f: rec[f] for f in fields})

    print('Done')


# --------------------------------------------------
if __name__ == '__main__':
    main()
