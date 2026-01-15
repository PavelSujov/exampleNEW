# Project Debug Rules (Non-Obvious Only)

## Virtual Environment Issues
- Watch for Unicode/Cyrillic character encoding issues in file paths
- When running pytest, ensure working directory is exampleNEW/ to avoid path issues
- Virtual environment must be activated in the correct directory to access project modules

## Data Processing Debugging
- Check for NaN values in numeric calculations using pd.to_numeric(..., errors="coerce")
- Verify that Russian column names are properly handled in pandas operations
- Look for SettingWithCopyWarning when modifying DataFrame copies