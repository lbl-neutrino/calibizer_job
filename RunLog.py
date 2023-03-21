#!/usr/bin/env python3

from dataclasses import dataclass
from typing import List, Optional

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# Module3 run log
SPREADSHEET_ID = '19kOYFh3UCpoBRHFm7KZPQs133jJaUSbRYCmbbW-EQ6I'
# RANGE_NAME = 'RunLog!G4:L'
# RANGE_NAME = 'RunLog!G556:L574'      # run2 w/ HV
RANGE_NAME = 'RunLog!G1312:L1513'      # run3 w/ HV as of 2023-03-16

@dataclass
class RunInfo:
    charge_fname: str
    light_fnames: List[str]
    drift_field: Optional[float] # kV/cm


class RunLog:
    def __init__(self):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        self._sheets_api = build('sheets', 'v4', credentials=creds).spreadsheets().values()
        self._load()

    def __getitem__(self, charge_fname):
        if charge_fname not in self._mapping:
            self._load()

        return self._mapping.get(charge_fname, None)

    def dict(self):
        return dict(self._mapping)

    def _load(self):
        self._mapping = {}
        values = self._sheets_api.get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME) \
            .execute().get('values', [])

        for row in values:
            if len(row) < 6:
                continue

            charge_fname = row[3]
            if not charge_fname.endswith('.h5'):
                continue

            if row[1].find('good') == -1:
                continue

            light_fnames = []
            drift_field = None

            if row[0]:
                drift_field = float(row[0])
            else:               # HACK
                drift_field = 0.5

            if len(row) >= 6 and row[5]:
                for light_fname in row[5].split(','):
                    light_fname = light_fname.strip()
                    # HACK to fix typo in run log
                    if light_fname.startswith('cd'):
                        light_fname = '0' + light_filename
                    # LCM, ACL, sum
                    valid_adcs = ['0cd8d63', '0cd913fa', '0cd9414a']
                    adc = light_fname.split('_')[0]
                    assert adc in valid_adcs
                    # HACK: ADC 0cd9414a gets the sum of the six SiPMs on each
                    # tile, for triggering. We don't actually want to pass its
                    # data to ndlar_flow. So let's just replace it with one of
                    # the two "full" ADCs. Doesn't matter which of the two,
                    # since ndlar_flow will automatically look for the other.
                    if adc == '0cd9414a':
                        light_fname = '0cd913fa' + light_fname[8:]
                    light_fnames.append(light_fname)

            info = RunInfo(charge_fname, light_fnames, drift_field)
            self._mapping[charge_fname] = info
