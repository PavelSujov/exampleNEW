# Project Coding Rules (Non-Obvious Only)

## Python Development
- Use pandas with Russian column names (e.g., "Материал пластины", "Толщина пластины, мкм")
- Apply .copy() when modifying DataFrames to avoid SettingWithCopyWarning
- Use pd.to_numeric(..., errors="coerce") for handling non-numeric values in calculations

## Project-Specific Patterns
- Module structure: data_loader, decrypting, plotting, analysis, with clear separation of concerns
- All functions require type hints and Google-style docstrings
- Use @st.cache_data decorator for expensive data loading operations
- Handle Cyrillic characters properly in file paths and data operations