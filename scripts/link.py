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


class Args(NamedTuple):
    """ Command-line arguments """
    sdtm_file: TextIO
    api_uri: str
    api_version: str
    api_key: str


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

    parser.add_argument('-k',
                        '--api_key',
                        help='API key',
                        metavar='str',
                        default=config.get('api_key'))

    parser.add_argument('-u',
                        '--api_uri',
                        help='UTS URI',
                        metavar='str',
                        default='https://uts-ws.nlm.nih.gov')

    parser.add_argument('-V',
                        '--api_version',
                        help='API version',
                        metavar='str',
                        default='current')

    args = parser.parse_args()

    return Args(args.sdtm_file, args.api_uri, args.api_version, args.api_key)


# --------------------------------------------------
def main() -> None:
    """ Make a jazz noise here """

    args = get_args()
    tgt = get_tgt(args.api_key)
    pprint(f'TGT {tgt}')

    reader = csv.DictReader(args.sdtm_file, delimiter='\t')

    for rec in reader:
        pprint(rec)

        if code := rec.get('Code'):
            if res := query(args, tgt, code):
                pprint(res)
                break


# --------------------------------------------------
def get_tgt(api_key: str) -> str:
    """ Get TGT """

    uri = 'https://utslogin.nlm.nih.gov'
    auth_endpoint = '/cas/v1/api-key'
    params = {'apikey': api_key}
    headers = {
        'Content-type': 'application/x-www-form-urlencoded',
        'Accept': 'text/plain',
        'User-Agent': 'python'
    }
    req = requests.post(uri + auth_endpoint, data=params, headers=headers)
    response = fromstring(req.text)
    return response.xpath('//form/@action')[0]


# --------------------------------------------------
def get_ticket(tgt: str) -> str:
    """ Get ticket """

    params = {'service': 'http://umlsks.nlm.nih.gov'}
    headers = {
        'Content-type': 'application/x-www-form-urlencoded',
        'Accept': 'text/plain',
        'User-Agent': 'python'
    }
    req = requests.post(tgt, data=params, headers=headers)
    return req.text


# --------------------------------------------------
def query(args: Args, tgt: str, term: str) -> Optional[str]:
    """ Query """

    uri = args.api_uri + "/rest/search/" + args.api_version
    ticket = get_ticket(tgt)
    params = {'string': term, 'ticket': ticket, 'pageNumber': 1}
    req = requests.get(uri, params=params)
    req.encoding = 'utf-8'
    res = json.loads(req.text)
    pprint(res)

    if 'error' in res:
        print(f"{term}: {res['error']}", file=sys.stderr)

    if 'result' in res:
        return res['result']


# --------------------------------------------------
if __name__ == '__main__':
    main()
