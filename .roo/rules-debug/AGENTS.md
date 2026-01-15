# Project Debug Rules (Non-Obvious Only)

## Virtual Environment
- Always ensure the virtual environment is activated before debugging: `venv\Scripts\activate`
- Python interpreter should be set to the one in the venv directory
- Debug console may need specific PYTHONPATH settings to recognize project modules

## Data Files
- Excel files in DevelopNEW data/ directory may require specific libraries like pandas and openpyxl
- Jupyter notebooks may need special kernel configuration to work with the virtual environment