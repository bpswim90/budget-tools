# Code Review: budget-tools

**Reviewed:** 2025-12-13
**Files Reviewed:** 5 source files, 3 test files, configuration files

---

## Summary

This is a CLI tool for importing bank CSV files to Google Sheets for budget tracking. The codebase is relatively small (~300 lines of Python) and accomplishes its purpose. However, there are several issues ranging from configuration problems to code quality improvements.

**Overall Score:** 6.5/10

---

## High Priority Issues

### 1. Resource Leaks - Files Not Properly Closed

**Locations:**
- `main.py:14`
- `csv_utils.py:72`
- `csv_utils.py:109`

**Severity:** High

Files are opened without context managers (`with` statement), risking resource leaks:

```python
# main.py:14
output_file = open('temp.csv', 'w', newline='', encoding="utf-8")
# ... file used ...
output_file.close()  # Only closed at line 29
```

If an exception occurs between open and close, the file handle leaks.

**Recommendation:** Use context managers:

```python
with open('temp.csv', 'w', newline='', encoding="utf-8") as output_file:
    # ... file operations ...
```

---

### 2. Code Executed at Module Import

**Location:** `main.py:41-45`

**Severity:** High

```python
try:
    import_files_to_sheets()
except KeyboardInterrupt:
    os.remove('temp.csv')
    raise
```

This code runs immediately when the module is imported, preventing:
- Using the module as a library
- Proper unit testing of `import_files_to_sheets()`

**Recommendation:** Use the standard pattern:

```python
if __name__ == "__main__":
    try:
        import_files_to_sheets()
    except KeyboardInterrupt:
        os.remove('temp.csv')
        raise
```

---

### 3. Global Config Loading at Import Time

**Locations:**
- `main.py:9`
- `csv_utils.py:7`

**Severity:** High

```python
config = load_config()  # Runs at import time
```

Issues:
- If `budgetConfig.json` is missing, import fails immediately
- Makes unit testing difficult (requires monkeypatching)
- Config loaded twice (once per module)

**Recommendation:** Load config lazily or pass as parameter to functions.

---

## Medium Priority Issues

### 4. No Error Handling

**Severity:** Medium

The codebase has no exception handling for:
- Missing/malformed `budgetConfig.json`
- Invalid CSV files
- Google Sheets API errors (rate limits, auth failures)
- Missing `csv/` directory
- Network connectivity issues

**Recommendation:** Add try/except blocks with meaningful error messages.

---

### 5. Hardcoded Temp File Path

**Locations:** `main.py:14,38,44`, `csv_utils.py:109`

**Severity:** Medium

`temp.csv` is hardcoded in multiple places. If two instances run simultaneously, they'd conflict.

**Recommendation:** Use `tempfile.NamedTemporaryFile()` or pass the temp file path as a parameter.

---

### 6. Bank Detection Logic is Fragile

**Location:** `main.py:24-27`

**Severity:** Medium

```python
if filename.lower().startswith(APPLE):
    csv_utils.copy_csv_to_temp_file(filename, APPLE, output_writer)
else:
    csv_utils.copy_csv_to_temp_file(filename, ALLY, output_writer)
```

Any CSV not starting with "apple" is assumed to be Ally. This will silently misprocess CSV files from other banks.

**Recommendation:** Explicitly check for Ally files and raise an error for unknown formats.

---

## Low Priority Issues

### 7. Unnecessary `elif` After `continue`

**Location:** `csv_utils.py:82-85`

**Severity:** Low (pylint warning)

```python
if reader.line_num == 1:
    continue
elif skip_row(row, desc_idx):  # 'elif' unnecessary after 'continue'
    continue
```

**Recommendation:** Change `elif` to `if`.

---

### 8. Incomplete Test Coverage for string_utils

**Location:** `tests/test_string_utils.py`

**Severity:** Low

Only tests negative-to-positive conversion:

```python
def test_flip_sign_of_amount():
    amount = '-23.45'
    assert flip_sign_of_amount(amount) == '23.45'
```

Missing test for positive-to-negative conversion.

**Recommendation:** Add parametrized tests for both cases.

---

### 9. No Type Annotations

**Severity:** Low

No type hints throughout the codebase. This reduces IDE support and makes the code harder to understand.

**mypy output:**
```
budget/csv_utils.py:2: error: Skipping analyzing "ezsheets": module is installed, but missing library stubs
budget/main.py:3: error: Skipping analyzing "pyinputplus": module is installed, but missing library stubs
```

**Recommendation:** Add type hints and ignore third-party modules without stubs.

---

### 10. Magic Numbers in CSV_TYPES

**Location:** `csv_utils.py:10-23`

**Severity:** Low

Index values are magic numbers without explanation:

```python
APPLE: {
    'dateIdx': 0,
    'descIdx': 2,
    'categoryIdx': 4,
    'amountIdx': 6
}
```

Why is description at index 2 but category at index 4? No documentation.

**Recommendation:** Add comments explaining the CSV column structure.

---

## Security Considerations

### 11. Token Files in Repository

**Locations:**
- `token-drive.pickle`
- `token-sheets.pickle`
- `budget/token-drive.pickle`
- `budget/token-sheets.pickle`

These contain OAuth tokens for Google APIs. While `.gitignore` may exclude them, they exist in the working directory and could be accidentally committed.

**Recommendation:** Ensure these are in `.gitignore` and consider storing them in a secure location like `~/.config/budget-tools/`.

---

## Positive Observations

1. **Clean separation of concerns** - Functions are well-organized with single responsibilities
2. **Good docstrings** - Most functions have clear docstrings
3. **Consistent encoding** - All file operations use `encoding="utf-8"`
4. **Parameterized tests** - Good use of `@pytest.mark.parametrize` for test data
5. **Test fixtures** - Proper use of `conftest.py` for test configuration
6. **pylint score of 9.65/10** - Code is generally clean

---

## Static Analysis Results

### pylint (9.65/10)
```
csv_utils.py:82: R1724: Unnecessary "elif" after "continue"
csv_utils.py:72: R1732: Consider using 'with' for resource-allocating operations
csv_utils.py:109: R1732: Consider using 'with' for resource-allocating operations
main.py:14: R1732: Consider using 'with' for resource-allocating operations
```

### mypy
```
2 errors (missing stubs for ezsheets and pyinputplus)
```

### pytest
```
17 passed
```

---

## Recommended Priority Order for Fixes

1. Add `if __name__ == "__main__":` guard in `main.py`
2. Convert file operations to use context managers
3. Improve bank detection logic
4. Add basic error handling
5. Add type annotations (optional but recommended)
