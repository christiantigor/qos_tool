#!/usr/bin/env python
import sys
from argparse import ArgumentParser
from json import dumps
import requests

# Contributed by Dangra (https://gist.github.com/dangra)

# Example Usage:
# 
#    $ ./locationapi.py --token XXXX --mcc 748 --mnc 7 66862/9020
# Output:
#    {'token': 'XXXX', 'mnc': 7, 'mcc': 748, 'cells': [{'lac': 9020, 'cid': 66862}]}
#    {u'status': u'ok', u'lat': -34.64405, u'balance': 38, u'lon': -54.16642}
#    https://maps.google.com/?q=-34.64405,-54.16642
#

def _cid_slash_lac(txt):
    cid, lac = txt.split('/')
    return int(cid), int(lac)


def main():
    ap = ArgumentParser()
    ap.add_argument('--token', default= '114087104419')
    ap.add_argument('--endpoint', default='http://ap1.unwiredlabs.com/v2/process.php')
    ap.add_argument('--mcc', type=int, default=510)  # Indonesia
    ap.add_argument('--mnc', type=int, default=01)  # Indosat
    ap.add_argument('cells', nargs='+', type=_cid_slash_lac)
    args = ap.parse_args()
    # locationapi accepts up to 5 cells per call
    assert len(args.cells) <= 5

    payload = {
        'token': args.token,
        'mcc': args.mcc,
        'mnc': args.mnc,
        'cells': [{'cid': cid, 'lac': lac} for cid, lac in args.cells],
    }
    print payload
    rsp = requests.post(url=args.endpoint,
                        data=dumps(payload),
                        headers={'content-encoding': 'application/json'})

    o = rsp.json()
    print o
    if o.get('status') == 'ok':
        print 'https://maps.google.com/?q={lat},{lon}'.format(**o)


if __name__ == '__main__':
    sys.exit(main())

