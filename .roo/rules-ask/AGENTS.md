# Project Documentation Rules (Non-Obvious Only)

## Project Context
- This is a semiconductor wafer cutting disc analysis application with interactive visualization
- Russian-language column names in data files are intentional (not encoding errors)
- Excel files contain critical domain-specific data for disc cutting parameters

## File Organization
- Data files in DevelopNEW data/ use Russian column names that must be referenced exactly
- The application allows users to upload custom databases with the same structure
- Kerf width slider has 5 μm step for precision control (not the default 25 μm)