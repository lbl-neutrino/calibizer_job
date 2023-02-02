#!/usr/bin/env python3

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# Module3 run log
SPREADSHEET_ID = '19kOYFh3UCpoBRHFm7KZPQs133jJaUSbRYCmbbW-EQ6I'
RANGE_NAME = 'RunLog!G4:J'

def get_hv_dict():
    "Returns mapping of filename to drift field (kV/cm)"
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    service = build('sheets', 'v4', credentials=creds)

    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=RANGE_NAME).execute()
    values = result.get('values', [])

    mapping = {}
    for row in values:
        if len(row) < 4:
            continue
        field, fname = row[0], row[3]
        if not fname.endswith('.h5'):
            continue
        field = float(field) if field else 0.0
        mapping[fname] = field

    return mapping
