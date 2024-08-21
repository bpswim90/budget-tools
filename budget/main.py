import csv
import os
import pyinputplus as pyip
import csvUtils
from configUtils import loadConfig
from constants import APPLE, ALLY


config = loadConfig()


def import_files_to_sheets():
    """Combine all operations to import & upload the csv files"""
    output_file = open('temp.csv', 'w', newline='')
    output_writer = csv.writer(output_file)
    output_writer.writerow(['date', 'category', 'description', 'amount'])

    # Write to temp combined CSV
    for filename in os.listdir(config['baseInputPath']):
        if not filename.endswith('.csv'):
            continue
        print('Reading from csv file: ' + filename + "...")

        if filename.lower().startswith(APPLE):
            csvUtils.copyCsvToTempFile(filename, APPLE, output_writer)
        else:
            csvUtils.copyCsvToTempFile(filename, ALLY, output_writer)

    output_file.close()

    new_sheet_name = pyip.inputStr(
        prompt='What would you like the new spreadsheet to be titled?\n')

    # Upload from temp csv to sheets
    csvUtils.uploadCsvToSheets(new_sheet_name)

    # Delete temp file
    os.remove('temp.csv')


try:
    import_files_to_sheets()
except KeyboardInterrupt:
    os.remove('temp.csv')
    raise
