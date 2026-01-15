# Project Architecture Rules (Non-Obvious Only)

## Project Structure
- The exampleNEW/ directory serves as a reference implementation and should inform architectural decisions for new development
- Data-driven approach is central to the project with Excel and Jupyter files in DevelopNEW data/ directory
- Virtual environment setup is essential for isolating dependencies

## Development Approach
- Follow the pattern established in exampleNEW/ when designing new components
- Consider data processing capabilities as a core architectural element given the nature of the data files
- Plan for integration with Excel and Jupyter notebook data sources from the beginning