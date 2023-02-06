#!/usr/bin/env python3

# NOTE: run_data.py: ``e_field`` run list file units are V/cm.
# Run log spreadsheet: kV/cm
# And just for extra confusion, RunData.yaml uses kV/mm

from RunLog import RunLog, RunInfo

HEADER = 'e_field charge_filename light_filename charge_thresholds light_samples'

DEFAULT_LIGHT_SAMPLES = 1024

def format_line(info: RunInfo) -> str:
    e_field = '%.3f' % (info.drift_field * 1000) if info.drift_field else '-'
    charge_filename = info.charge_fname
    light_filename = info.light_fname if info.light_fname else '-'
    charge_thresholds = 'medm'
    light_samples = str(DEFAULT_LIGHT_SAMPLES)

    return f'{e_field} {charge_filename} {light_filename} {charge_thresholds} {light_samples}'


def main():
    runlog = RunLog()

    print(HEADER)

    for info in RunLog().dict().values():
        print(format_line(info))


if __name__ == '__main__':
    main()
