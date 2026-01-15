# AGENTS.md

This file provides guidance to agents when working with code in this repository.

## Project Overview
- Python-based project with virtual environment setup
- Project name suggests development of an interactive technical database/configurator for cutting discs for semiconductor plates
- Located in the DevelopNEW directory with exampleNEW as a reference implementation

## Build/Lint/Test Commands
- Use `venv\Scripts\activate` to activate the Python virtual environment (Windows)
- Use `python -m pip install -r requirements.txt` to install dependencies (after creating requirements.txt)
- Use `python -m pytest` to run tests (after implementing tests)
- Use `python -m flake8` or `python -m black` for code linting/formatting (after installing these tools)

## Code Style Guidelines
- Follow PEP 8 Python style guidelines
- Use meaningful variable and function names
- Include docstrings for all functions and classes
- Use type hints for function parameters and return values
- Organize imports in standard library, third-party, then local modules

## Project Structure
- `DevelopNEW data/` - Contains data files including Jupyter notebooks and Excel files for the technical database
- `exampleNEW/` - Reference implementation of the interactive technical database/configurator
- `venv/` - Python virtual environment
- `venv_activation_instructions.txt` - Instructions for activating the virtual environment