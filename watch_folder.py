#!/usr/bin/env python3

import argparse
from pathlib import Path
import time

POLL_INTERVAL_SEC = 60
MIN_AGE_SEC = 60

def watch_folder(indir, outfile):
    items = set()

    if Path(outfile).exists():
        items = set(line.strip() for line in open(outfile))

    with open(outfile, 'a') as outf:
        while True:
            for p in Path(indir).glob('*.h5'):
                abspath = str(p.absolute())

                if abspath in items:
                    continue

                if time.time() - p.stat().st_mtime < 60:
                    continue

                outf.write(f'{abspath}\n')
                items.add(abspath)
                print(f'Added {abspath}')

            outf.flush()
            print('Sleeping...')
            time.sleep(POLL_INTERVAL_SEC)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('-i', '--indir', required=True)
    ap.add_argument('-o', '--outfile', required=True)
    args = ap.parse_args()

    watch_folder(args.indir, args.outfile)


if __name__ == '__main__':
    main()
