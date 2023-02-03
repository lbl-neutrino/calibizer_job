#!/usr/bin/env python3

from dataclasses import dataclass

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# Module3 run log
SPREADSHEET_ID = '19kOYFh3UCpoBRHFm7KZPQs133jJaUSbRYCmbbW-EQ6I'
RANGE_NAME = 'RunLog!G4:L'

@dataclass
class RunInfo:
    charge_fname: str
    light_fname: str = ''
    drift_field: float = 0.0


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
            if len(row) < 4:
                continue

            charge_fname = row[3]
            if not charge_fname.endswith('.h5'):
                continue

            light_fname = ''
            drift_field = 0.0

            if row[0]:
                drift_field = float(row[0])

            if len(row) >= 6 and row[5]:
                light_fname = row[5]

            info = RunInfo(charge_fname, light_fname, drift_field)
            self._mapping[charge_fname] = info
