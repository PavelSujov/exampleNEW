# AGENTS.md

This file provides guidance to agents when working with code in this repository.

## Project Overview
- Streamlit-based interactive database for semiconductor wafer cutting disc analysis
- Uses pandas for data processing, plotly for visualization, and openpyxl for Excel support
- Located in exampleNEW directory with Russian-language column names in data files

## Build/Lint/Test Commands
- Activate virtual env: `cd exampleNEW && venv\Scripts\activate`
- Install dependencies: `pip install -r requirements.txt`
- Run tests: `python -m pytest test_analysis.py -v`
- Lint code: `python -m flake8 . --max-line-length=120`
- Format code: `python -m black .`

## Code Style Guidelines
- Use snake_case for function and variable names
- Include type hints for all functions (e.g., `def func(data: pd.DataFrame) -> Dict[str, float]:`)
- Docstrings in Google format with Args/Returns sections
- Handle Russian column names in pandas operations (e.g., "Толщина пластины, мкм")
- Use f-strings for formatting, avoid non-ASCII characters in code