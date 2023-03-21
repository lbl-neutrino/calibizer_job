#!/usr/bin/env python3

# NOTE: run_data.py: ``e_field`` run list file units are V/cm.
# Run log spreadsheet: kV/cm
# And just for extra confusion, RunData.yaml uses kV/mm

from collections import defaultdict
from functools import lru_cache
from pathlib import Path
import sys

from RunLog import RunLog, RunInfo

HEADER = 'e_field charge_filename light_filename charge_thresholds light_samples'

DEFAULT_LIGHT_SAMPLES = 1024

BASEDIR = Path('/global/cfs/cdirs/dune/www/data/Module3/run3')


@lru_cache
def read_lightdict() -> dict[str, Path]:
    result = defaultdict(lambda: '-')
    lightbase = BASEDIR.joinpath('LRS')
    for path in lightbase.rglob('*.data'):
        result[path.name] = path
    return result


def format_line(info: RunInfo) -> str:
    e_field = '%.3f' % (info.drift_field * 1000) if info.drift_field else '-'
    charge_filename = info.charge_fname
    # light_filename = ','.join(info.light_fnames) if info.light_fnames else '-'
    charge_thresholds = 'medm'
    light_samples = str(DEFAULT_LIGHT_SAMPLES)

    # packet_path = BASEDIR.joinpath('packet', 'ramp_up',
    #                                info.charge_fname.replace('-binary-', '-packet-'))
    packet_path = BASEDIR.joinpath('packet', 'tpc12',
                                   info.charge_fname.replace('-binary-', '-packet-'))
    if not packet_path.exists():
        print('WTF', packet_path, file=sys.stderr)
        return ''

    light_paths = ','.join(str(read_lightdict()[fname]) for fname in info.light_fnames)

    return f'{e_field} {packet_path} {light_paths} {charge_thresholds} {light_samples}\n'


def is_good(info: RunInfo) -> bool:
    return True
    return info.drift_field and len(info.light_fnames) >= 1 \
        and all(fname.endswith('.data') for fname in info.light_fnames) \
        and info.charge_fname.endswith('.h5')


def main():
    runlog = RunLog()

    print(HEADER)

    for info in RunLog().dict().values():
        if is_good(info):
            print(format_line(info), end='')


if __name__ == '__main__':
    main()
