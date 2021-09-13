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
from concepts import SnomedConcept


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
                        help='Snomed file',
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
    reader = csv.DictReader(args.file, delimiter='\t')
    for i, rec in enumerate(reader, start=1):
        # pprint(rec)
        print(f"{i:9,}: {rec['concept_id']}")
        concept, _ = SnomedConcept.get_or_create(**rec)

    print('Done')


# --------------------------------------------------
if __name__ == '__main__':
    main()
