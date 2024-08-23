import csv
import os
import pyinputplus as pyip
import csv_utils
from config_utils import load_config
from constants import APPLE, ALLY


config = load_config()


def import_files_to_sheets():
    """Combine all operations to import & upload the csv files"""
    output_file = open('temp.csv', 'w', newline='', encoding="utf-8")
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

    output_file.close()

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
