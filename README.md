# budget-tools

Practicing Python by building tools to automate my budgeting.

## Why?

On a monthly basis I create a google sheet to aggregate and document all my spending for that month, aka a budget.

To do this, I used to download csv files from my bank and manually copied the data over, categorizing each transaction so I could track over time how my spending in different categories (groceries, entertainment, etc.) changes over time.

This program seeks to automate a lot of that process by automatically importing and uploading the csv files to my google sheet, and categorizing the transactions when possible.

## How does it work?

The raw csv files go into the `/csv` folder in the root. (Currently I just have two CSVs that I need to import.) `budget.py` combines/translates the files into a temporary csv (the CSVs have different column order so need to be mapped).

During the process of translation, it will also skip over rows that are irrelevant to my budget, and also attempt to categorize the transactions based on the description or category found in the CSV. These mappings are configured in the `budgetConfig.json` file.

Once the temp file has been created, it will attempt to upload the file to google sheets, and then will delete the temp CSV.

## Stuff I learned

- Working with files in Python, and CSV files in particular
- Loading in a "config" file and the different options available in Python (.ini, .toml, .json, and more...). I ended up going with json due to my desire to have spaces and commas in the keys
- General working with different data structures and control flow in python

## Stuff I might work on

- [ ] Create new sheet from the template and import the CSVs t othat sheet
- [ ] Add ability to specify name of the new sheet via command line
- [ ] Maybe break out budget.py into a couple modules to improve readability
- [ ] Look into adding tests - mock out the structure of the CSV files I use to use in tests
- [ ] Could I turn this into a deployed API? Ability to update the configurations via a JSON API, configurations stored in a DB, etc...
- [ ] Then could there be a UI to interact with the API, that would enable you to upload the CSVs, change configurations, etc.
