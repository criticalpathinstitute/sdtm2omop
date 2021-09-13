#!/usr/bin/env python3
"""
Author : Ken Youens-Clark <kyclark@gmail.com>
Date   : 2021-08-31
Purpose: Link SDTM terms
"""

import argparse
import csv
import json
import requests
import sys
from pprint import pprint
from lxml.html import fromstring
from dotenv import dotenv_values
from typing import NamedTuple, Optional, TextIO
from concepts import UmlsConcept, SnomedConcept


class Args(NamedTuple):
    """ Command-line arguments """
    sdtm_file: TextIO
    db_name: str
    out_file: TextIO


# --------------------------------------------------
def get_args() -> Args:
    """ Get command-line arguments """

    config = dotenv_values()
    parser = argparse.ArgumentParser(
        description='Link SDTM terms',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('sdtm_file',
                        help='SDTM file',
                        metavar='FILE',
                        type=argparse.FileType('rt'))

    parser.add_argument('-d',
                        '--db_name',
                        help='SQLite db name',
                        metavar='str',
                        default='concepts.db')

    parser.add_argument('-o',
                        '--outfile',
                        help='Output file',
                        metavar='str',
                        type=argparse.FileType('wt'),
                        default='umls_snomed_concepts.tsv')

    args = parser.parse_args()

    return Args(args.sdtm_file, args.db_name, args.outfile)


# --------------------------------------------------
def main() -> None:
    """ Make a jazz noise here """

    args = get_args()
    reader = csv.DictReader(args.sdtm_file, delimiter='\t')
    seen = set()

    print('\t'.join([
        'sdtm_ct_code', 'cdisc_submission_value', 'cui', 'snomed_code',
        'concept_id'
    ]),
          file=args.out_file)

    for rec in reader:
        # pprint(rec)
        if code := rec.get('Code'):
            print('Searching for "{}" ({})'.format(code,
                                                   rec['CDISC Synonym(s)']))
            if res := UmlsConcept.select().where(UmlsConcept.code == code):
                for r in res:
                    if res2 := UmlsConcept.select().where(
                        (UmlsConcept.cui == r.cui)
                            & (UmlsConcept.source_name == 'SNOMEDCT_US')):
                        for r2 in res2:
                            if snomed := SnomedConcept.select().where(
                                    SnomedConcept.concept_code == r2.code):
                                for sno in snomed:
                                    val = '\t'.join([
                                        code,
                                        rec['CDISC Synonym(s)'],
                                        r2.cui,
                                        sno.concept_code,
                                        sno.concept_id,
                                    ])

                                    if val in seen:
                                        continue

                                    seen.add(val)
                                    print(val, file=args.out_file)

    print(f'Done, see output in "{args.out_file.name}"')


# --------------------------------------------------
if __name__ == '__main__':
    main()
