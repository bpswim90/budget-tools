import csv
import ezsheets
from string_utils import flip_sign_of_amount
from config_utils import load_config
from constants import APPLE, ALLY

config = load_config()

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


def skip_row(row, desc_idx):
    """Skip a csv row from being imported"""
    items_to_skip = tuple(config['itemsToSkip'])
    if row[desc_idx].startswith(items_to_skip):
        return True
    return False


def category_matches_config_category(csv_category, budget_category):
    """Check whether a given csv category matches the desired category in sheets"""
    config_category_list = config['categoryFromCsvCategory'][budget_category]
    result = any(csv_category.lower() in configCategory.lower()
                 for configCategory in config_category_list)
    return result


def get_category(row, category_idx):
    """Get sheets category that matches the csv category for a given row"""
    csv_category = row[category_idx]

    for budget_category in config['categoryFromCsvCategory'].keys():
        if category_matches_config_category(csv_category, budget_category):
            return budget_category
    return ''


def desc_matches_category(desc, category):
    """Check whether a given description from the csv matches a category in sheets"""
    match_list = config['categoryFromDesc'][category]
    result = any(word.lower() in desc.lower() for word in match_list)
    return result


def get_category_from_desc(row, desc_idx):
    """Get category from the csv description for a csv row"""
    desc = row[desc_idx]

    for category in config['categoryFromDesc'].keys():
        if desc_matches_category(desc, category):
            return category
    return ''


def copy_csv_to_temp_file(filename, csv_type, output_writer):
    """Translate one of the input csv's into the temp csv"""
    filepath = config['baseInputPath'] + filename
    transactions = open(filepath, encoding="utf-8")
    reader = csv.reader(transactions)

    date_idx = CSV_TYPES[csv_type]['dateIdx']
    desc_idx = CSV_TYPES[csv_type]['descIdx']
    category_idx = CSV_TYPES[csv_type]['categoryIdx']
    amount_idx = CSV_TYPES[csv_type]['amountIdx']

    for row in reader:
        # Skip header row
        if reader.line_num == 1:
            continue
        elif skip_row(row, desc_idx):
            continue

        # First try to get category from description,
        # then try to get it from csv category
        category = get_category_from_desc(row, desc_idx)

        if not category and category_idx is not None:
            category = get_category(row, category_idx)

        # Copy over date value
        date = row[date_idx]

        # Copy over description
        desc = row[desc_idx]

        # Copy over $ amount of item
        amount = row[amount_idx] if csv_type == ALLY else flip_sign_of_amount(
            row[amount_idx])

        output_writer.writerow([date, category, desc, amount])


def upload_csv_to_sheets(new_sheet_name):
    """Uploads the temp csv to sheets"""
    temp_csv = open('temp.csv', 'r', encoding="utf-8")
    reader = csv.reader(temp_csv)

    date_col = []
    category_col = []
    desc_col = []
    amount_col = []

    for row in reader:
        date_col.append(row[0])
        category_col.append(row[1])
        desc_col.append(row[2])
        amount_col.append(row[3])

    template_ss = ezsheets.Spreadsheet(config['budgetTemplateId'])
    template_sheet = template_ss.sheets[0]

    new_sheet = ezsheets.createSpreadsheet(new_sheet_name)
    template_sheet.copyTo(new_sheet)
    # Delete and replace the default sheet 1 of the new spreadsheet
    del new_sheet[0]
    budget_sheet = new_sheet[0]
    budget_sheet.title = 'Sheet 1'

    budget_sheet.updateColumn(1, date_col)
    budget_sheet.updateColumn(2, category_col)
    budget_sheet.updateColumn(3, desc_col)
    budget_sheet.updateColumn(4, amount_col)
