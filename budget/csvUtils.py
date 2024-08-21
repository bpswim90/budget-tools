import csv
import ezsheets
import json
from stringUtils import flipSignOfAmount
from constants import APPLE, ALLY

with open('../budgetConfig.json', 'r') as f:
    config = json.load(f)

# Describes which index to look at in the individual csv transaction files
CSV_TYPES = {
    APPLE: {
        'dateIdx': 0,
        'descIdx': 2,
        'categoryIdx': 4,
        'amountIdx': 6
    },
    ALLY: {
        'dateIdx': 0,
        'descIdx': 4,
        'categoryIdx': None,
        'amountIdx': 2
    }
}


def skipRow(row, descIdx):
    """Skip a csv row from being imported"""
    itemsToSkip = tuple(config['itemsToSkip'])
    if row[descIdx].startswith(itemsToSkip):
        return True
    return False


def categoryMatchesConfigCategory(csvCategory, budgetCategory):
    """Check whether a given csv category matches the desired category in sheets"""
    configCategoryList = config['categoryFromCsvCategory'][budgetCategory]
    result = any(csvCategory.lower() in configCategory.lower()
                 for configCategory in configCategoryList)
    return result


def getCategory(row, categoryIdx):
    """Get sheets category that matches the csv category for a given row"""
    csvCategory = row[categoryIdx]

    for budgetCategory in config['categoryFromCsvCategory'].keys():
        if categoryMatchesConfigCategory(csvCategory, budgetCategory):
            return budgetCategory
    return ''


def descMatchesCategory(desc, category):
    """Check whether a given description from the csv matches a category in sheets"""
    matchList = config['categoryFromDesc'][category]
    result = any(word.lower() in desc.lower() for word in matchList)
    return result


def getCategoryFromDesc(row, descIdx):
    """Get category from the csv description for a csv row"""
    desc = row[descIdx]

    for category in config['categoryFromDesc'].keys():
        if descMatchesCategory(desc, category):
            return category
    return ''


def copyCsvToTempFile(filename, csvType, outputWriter):
    """Translate one of the input csv's into the temp csv"""
    filepath = config['baseInputPath'] + filename
    transactions = open(filepath)
    reader = csv.reader(transactions)

    dateIdx = CSV_TYPES[csvType]['dateIdx']
    descIdx = CSV_TYPES[csvType]['descIdx']
    categoryIdx = CSV_TYPES[csvType]['categoryIdx']
    amountIdx = CSV_TYPES[csvType]['amountIdx']

    for row in reader:
        # Skip header row
        if reader.line_num == 1:
            continue
        elif skipRow(row, descIdx):
            continue

        # First try to get category from description,
        # then try to get it from csv category
        category = getCategoryFromDesc(row, descIdx)

        if not category and categoryIdx != None:
            category = getCategory(row, categoryIdx)

        # Copy over date value
        date = row[dateIdx]

        # Copy over description
        desc = row[descIdx]

        # Copy over $ amount of item
        amount = row[amountIdx] if csvType == ALLY else flipSignOfAmount(
            row[amountIdx])

        outputWriter.writerow([date, category, desc, amount])


def uploadCsvToSheets(newSheetName):
    """Uploads the temp csv to sheets"""
    tempCsv = open('temp.csv', 'r')
    reader = csv.reader(tempCsv)

    dateCol = []
    categoryCol = []
    descCol = []
    amountCol = []

    for row in reader:
        dateCol.append(row[0])
        categoryCol.append(row[1])
        descCol.append(row[2])
        amountCol.append(row[3])

    templateSs = ezsheets.Spreadsheet(config['budgetTemplateId'])
    templateSheet = templateSs.sheets[0]

    newSheet = ezsheets.createSpreadsheet(newSheetName)
    templateSheet.copyTo(newSheet)
    # Delete and replace the default sheet 1 of the new spreadsheet
    del newSheet[0]
    budgetSheet = newSheet[0]
    budgetSheet.title = 'Sheet 1'

    budgetSheet.updateColumn(1, dateCol)
    budgetSheet.updateColumn(2, categoryCol)
    budgetSheet.updateColumn(3, descCol)
    budgetSheet.updateColumn(4, amountCol)
