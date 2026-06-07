import csv
import os
import pickle
import socket
import ezsheets
import pyinputplus as pyip
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from budget import csv_utils
from budget.config_utils import load_config
from budget.constants import APPLE, ALLY

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]
TOKEN_FILES = ["token-sheets.pickle", "token-drive.pickle"]


def _ensure_google_tokens():
    creds = None
    for token_file in TOKEN_FILES:
        if os.path.exists(token_file):
            with open(token_file, "rb") as f:
                creds = pickle.load(f)
            break

    needs_auth = not creds or not creds.valid
    needs_save = needs_auth or not all(os.path.exists(f) for f in TOKEN_FILES)

    if needs_auth:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            with socket.socket() as s:
                s.bind(("", 0))
                free_port = s.getsockname()[1]
            flow = InstalledAppFlow.from_client_secrets_file("credentials-sheets.json", SCOPES)
            creds = flow.run_local_server(port=free_port)

    if needs_save:
        for token_file in TOKEN_FILES:
            with open(token_file, "wb") as f:
                pickle.dump(creds, f)


config = load_config()
_ensure_google_tokens()
ezsheets.init()


def import_files_to_sheets():
    """Combine all operations to import & upload the csv files"""
    with open('temp.csv', 'w', newline='', encoding="utf-8") as output_file:
        output_writer = csv.writer(output_file)
        output_writer.writerow(['date', 'category', 'description', 'amount'])

        # Write to temp combined CSV
        for filename in os.listdir(config['baseInputPath']):
            if not filename.endswith('.csv'):
                continue
            print('Reading from csv file: ' + filename + "...")

            if filename.lower().startswith(APPLE):
                csv_utils.copy_csv_to_temp_file(filename, APPLE, output_writer)
            else:
                csv_utils.copy_csv_to_temp_file(filename, ALLY, output_writer)

    new_sheet_name = pyip.inputStr(
        prompt='What would you like the new spreadsheet to be titled?\n')

    # Upload from temp csv to sheets
    csv_utils.upload_csv_to_sheets(new_sheet_name)

    # Delete temp file
    os.remove('temp.csv')


try:
    import_files_to_sheets()
except KeyboardInterrupt:
    os.remove('temp.csv')
    raise
