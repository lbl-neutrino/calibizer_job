#!/usr/bin/env python3

import os
from pathlib import Path
import shutil
from subprocess import call

import pandas as pd

# 250MB:
TESTFILE = '/global/cfs/cdirs/dune/www/data/Module3/packet/ramp_up/self_trigger_adc_calo_target-50-packet-2023_02_01_05_15_CET.h5'

# 1.4GB:
# TESTFILE = '/global/cfs/cdirs/dune/www/data/Module3/packet/ramp_up/self_trigger_adc_calo_target-50-packet-2023_02_03_08_48_CET.h5'
# We get 129GB out! keep-vwfms?!?

class Module3Worker:
    BASEDIR = Path('/global/cfs/cdirs/dune/www/data/Module3')

    def __init__(self, runlist_path='runlist_good.txt'):
        self.runlist = self.read_runlist(runlist_path)
        # self.lightdict = self.read_lightdict()

    @staticmethod
    def read_runlist(path: str) -> pd.DataFrame:
        return pd.read_csv(path, sep=r'\s+')

    # @classmethod
    # def read_lightdict(cls) -> dict[str, Path]:
    #     result = {}
    #     lightbase = cls.BASEDIR.joinpath('LRS')
    #     for path in lightbase.rglob('*.data'):
    #         result[path.name] = path
    #     return result

    def find_lightfile(self, packet_path: Path) -> Path:
        row = self.runlist.query(f'charge_filename == "{packet_path}"').iloc[0]
        return Path(row['light_filename'])
    #     rawname = self.get_rawname(packet_path)
    #     row = self.runlist.query(f'charge_filename == "{rawname}"').iloc[0]
    #     return self.lightdict[row['light_filename']]

    @staticmethod
    def get_outname(packet_path: Path) -> str:
        return packet_path.name.replace('-packet-', '-reco-')

    # @staticmethod
    # def get_rawname(packet_path: Path) -> str:
    #     return packet_path.name.replace('-packet-', '-binary-')

    @classmethod
    def get_outpath(cls, packet_path: Path) -> Path:
        # ramp_up
        reldir = packet_path.parent.relative_to(cls.BASEDIR.joinpath('packet'))
        # /global/cfs/cdirs/dune/www/data/Module3/reco/ramp_up
        outdir = cls.BASEDIR.joinpath('reco', reldir)
        # outdir.mkdir(parents=True, exist_ok=True)
        outname = cls.get_outname(packet_path)
        # /global/cfs/cdirs/dune/www/data/Module3/reco/ramp_up/self_trigger_adc_calo_target-50-reco-2023_02_01_05_15_CET.h5
        return outdir.joinpath(outname)

    @classmethod
    def get_tmppath(cls, packet_path: Path) -> Path:
        tmpdir = Path(os.getenv('SCRATCH')).joinpath('calibizer')
        tmpdir.mkdir(exist_ok=True)
        # /pscratch/sd/m/mkramer/self_trigger_adc_calo_target-50-reco-2023_02_01_05_15_CET.h5
        outname = cls.get_outname(packet_path)
        tmppath = tmpdir.joinpath(outname)
        return tmppath

    def process(self, packet_path):
        # /global/cfs/cdirs/dune/www/data/Module3/packet/ramp_up/self_trigger_adc_calo_target-50-packet-2023_02_01_05_15_CET.h5
        packet_path = Path(packet_path)
        assert packet_path.exists()
        assert packet_path.is_relative_to(self.BASEDIR.joinpath('packet'))
        assert packet_path.name.find('-packet-') != -1

        lightpath = self.find_lightfile(packet_path)
        assert lightpath.exists()

        outpath = self.get_outpath(packet_path)
        tmppath = self.get_tmppath(packet_path)
        tmppath.unlink(missing_ok=True)

        cmd = f'time ./run_module0_flow-module3.sh {packet_path} {lightpath} {tmppath}'
        retcode = call(cmd, shell=True)

        if retcode == 0:
            outpath.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(tmppath, outpath)


def main():
    mw = Module3Worker()
    mw.process(TESTFILE)


if __name__ == '__main__':
    main()
