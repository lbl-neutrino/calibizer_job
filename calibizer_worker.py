#!/usr/bin/env python3

# This worker now expects to receive an input file in runlist format (without
# the header).

import argparse
from pathlib import Path
import shutil
from subprocess import call
import sys
import time

from zeroworker import LockfileListReader, LockfileListWriter
# from zeroworker import ZmqListReader, ZmqListWriter

BASEDIR = '/global/cfs/cdirs/dune/www/data/Module2'
INDIR = f'{BASEDIR}/packetized'
OUTDIR = f'{BASEDIR}/charge_reco/v1'


def get_outpath_(path, outdir: str) -> Path:
    relpath = Path(path).relative_to(INDIR)
    assert relpath.name.find('-packet-') != -1, \
        '"{path}" does\'t have "-packet-" in its name, are you sure it\'s a packet file?'
    outname = relpath.name.replace('-packet-', '-reco-')
    out_relpath = relpath.parent.joinpath(outname)
    return Path(BASEDIR).joinpath(outdir, out_relpath)


def get_outpath(path) -> Path:
    return get_outpath_(path, OUTDIR)


def get_tmppath(path) -> Path:
    return get_outpath_(path, OUTDIR+'.tmp')


def process(chargepath, lightpaths, config):
    tmppath = get_tmppath(chargepath)
    tmppath.parent.mkdir(parents=True, exist_ok=True)
    tmppath.unlink(missing_ok=True) # don't want to append!

    print(f'PROCESSING {chargepath}')

    cmd = f'time ./run_module0_flow-{config}.sh {tmppath} {path} {" ".join(lightpaths)}'
    retcode = call(cmd, shell=True)

    if retcode == 0:
        outpath = get_outpath(chargepath)
        outpath.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(tmppath, outpath)

    return retcode


def main():
    sys.stdout.reconfigure(line_buffering=True)
    sys.stderr.reconfigure(line_buffering=True)

    ap = argparse.ArgumentParser()
    ap.add_argument('infile')
    ap.add_argument('-c', '--config', default='module3')
    ap.add_argument('--immortal', action='store_true')
    args = ap.parse_args()

    reader = LockfileListReader(args.infile)
    logger = LockfileListWriter(args.infile+'.done')

    with logger:
        while True:
            try:
                path = next(reader)
                retcode = process(path, args.config)
                logger.log(f'{path} {retcode}')
            except StopIteration:
                if args.immortal:
                    time.sleep(60)
                else:
                    break


if __name__ == '__main__':
    main()
