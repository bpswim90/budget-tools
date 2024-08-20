import csv, os
import json
import pyinputplus as pyip
import csvUtils 
from constants import APPLE, ALLY

with open('../budgetConfig.json', 'r') as f:
    config = json.load(f)

# Main function that combines all operations to import & upload the csv files
def importFilesToSheets():
    outputFile = open('temp.csv', 'w', newline='')
    outputWriter = csv.writer(outputFile)
    outputWriter.writerow(['date','category','description','amount'])

    # Write to temp combined CSV
    for filename in os.listdir(config['baseInputPath']):
        if not filename.endswith('.csv'):
            continue
        print('Reading from csv file: ' + filename + "...")

        if filename.lower().startswith(APPLE):
            csvUtils.copyCsvToTempFile(filename, APPLE, outputWriter)
        else:
            csvUtils.copyCsvToTempFile(filename, ALLY, outputWriter)

    outputFile.close()

    newSheetName = pyip.inputStr(prompt='What would you like the new spreadsheet to be titled?\n')

    # Upload from temp csv to sheets
    csvUtils.uploadCsvToSheets(newSheetName)

    # Delete temp file
    os.remove('temp.csv')

importFilesToSheets()



