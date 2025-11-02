# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Testing
```bash
pytest                    # Run all tests
pytest tests/test_csv_utils.py  # Run specific test file
```

### Code Quality
```bash
pylint budget/           # Lint the budget module
mypy budget/            # Type checking for budget module
```

### Running the Application
```bash
cd budget/
python main.py          # Interactive CSV import tool
```

## Architecture Overview

This is a CLI tool for automating the import of bank CSV files to Google Sheets for budget tracking.

### CLI Tool (`budget/` directory)
- **Purpose**: Interactive command-line tool for importing bank CSV files to Google Sheets
- **Entry point**: `budget/main.py`
- **Key components**:
  - `csv_utils.py`: CSV processing, Google Sheets integration via EZSheets library
  - `config_utils.py`: JSON configuration file loading (`budgetConfig.json`)
  - `string_utils.py`: Transaction amount and description processing
  - `constants.py`: Bank identifiers (APPLE, ALLY)

## Configuration System

### JSON Config (`budgetConfig.json`)
Used by CLI tool for:
- CSV file processing rules (`itemsToSkip`, `categoryFromDesc`, `categoryFromCsvCategory`)
- Google Sheets integration (`budgetTemplateId`)
- Bank-specific CSV column mappings

## Data Flow

1. Reads CSV files from `csv/` directory
2. Processes transactions using `budgetConfig.json` mappings
3. Combines into temporary CSV with normalized columns
4. Uploads to Google Sheets using EZSheets library
5. Prompts user for new sheet name

## Dependencies

- **Google Sheets**: EZSheets library for Google Sheets integration
- **Testing**: pytest with `pytest.ini` configuration setting `pythonpath = budget`
- **Code Quality**: pylint, mypy available in requirements.txt

## File Structure Notes

- CSV files are stored in `csv/` directory
- Google API credentials stored in `credentials-sheets.json` and token files
- Configuration template: `budgetConfig.json.example`