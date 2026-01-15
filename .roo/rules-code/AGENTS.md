# Project Coding Rules (Non-Obvious Only)

## Python Development
- Always activate the virtual environment before installing packages: `venv\Scripts\activate`
- Use Python 3.14.0 as specified in pyvenv.cfg
- Install dependencies with `pip install -r requirements.txt` (create requirements.txt first)
- Follow PEP 8 guidelines for code formatting
- Include type hints for all function parameters and return values
- Add docstrings to all functions and classes

## Project-Specific Patterns
- Data files are stored in the DevelopNEW data/ directory in various formats (Excel, Jupyter notebooks)
- exampleNEW/ directory contains reference implementation to follow for new development
- Use relative imports when referencing modules within the project