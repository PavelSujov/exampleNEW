# Interactive Database for Semiconductor Wafer Cutting Discs Analysis

## English Version

This Streamlit-based application provides an interactive interface for analyzing and visualizing data related to semiconductor wafer cutting using precision cutting discs. The application allows engineers and technicians to analyze cutting parameters, optimize processes, and make data-driven decisions to improve manufacturing efficiency.

### Live Application
Access the live application at: [https://examplenew.streamlit.app/](https://examplenew.streamlit.app/)

### Functional Capabilities
- **Data Filtering**: Interactive filters for materials, cut types, thickness ranges, and kerf width ranges
- **Visual Analytics**: Interactive plots showing relationships between cutting parameters and performance metrics
- **Article Decoding**: Tool to decode disc article numbers and retrieve specific parameter information
- **Performance Analysis**: Metrics for chipping, performance rates, and disc lifespan
- **Parameter Optimization**: Recommendations for optimal cutting settings based on material properties
- **Custom Database Upload**: Users can upload their own database files for analysis

### Technological Significance
The application leverages modern data science techniques to transform raw cutting process data into actionable insights. By using pandas for data manipulation and Plotly for interactive visualizations, it provides a sophisticated analytical platform that enables engineers to identify patterns, correlations, and optimization opportunities in the wafer cutting process.

### Economic Impact
- **Process Optimization**: Reduces material waste by identifying optimal cutting parameters
- **Equipment Efficiency**: Extends disc lifespan through better parameter selection
- **Quality Control**: Minimizes chipping and defects, reducing rejection rates
- **Cost Reduction**: Improves overall manufacturing efficiency and reduces operational costs
- **Decision Support**: Enables evidence-based decisions for process improvements

### Development and Deployment
- **Docker Support**: Containerized application for consistent deployment
- **GitHub Actions**: Automated testing and deployment pipeline
- **Test Coverage**: Comprehensive unit tests ensuring code quality
- **Code Quality**: Follows PEP 8 standards with type hints and documentation

---

## Russian Version / Русская версия

[RU_README.md](RU_README.md)

---

## Table of Contents / Содержание
- [Installation / Установка](#installation--установка)
- [Usage / Использование](#usage--использование)
- [Features / Функции](#features--функции)
- [Technology Stack / Технологии](#technology-stack--технологии)
- [Testing / Тестирование](#testing--тестирование)
- [Deployment / Развертывание](#deployment--развертывание)

---

## Installation / Установка

### Prerequisites / Необходимые компоненты
- Python 3.14+
- pip package manager

### Setup / Настройка
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd exampleNEW
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   source venv/bin/activate  # On macOS/Linux
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   streamlit run app.py
   ```

## Usage / Использование

### Local Development / Локальная разработка
1. Activate the virtual environment
2. Run `streamlit run app.py`
3. Access the application at `http://localhost:8501`

### Docker Deployment / Docker-развертывание
1. Build the image:
   ```bash
   docker build -t streamlit-disc-analysis-app .
   ```

2. Run the container:
   ```bash
   docker run -p 8501:8501 streamlit-disc-analysis-app
   ```

## Features / Функции

### Core Features / Основные функции
- Interactive data filtering and visualization
- Disc article decoding with parameter extraction
- Performance metrics and analysis
- Custom database upload capability
- Multi-language support (English/Russian)

### Data Analysis / Анализ данных
- Material-specific statistics
- Cut type analysis
- Performance trend identification
- Parameter optimization recommendations

## Technology Stack / Технологии

### Backend Technologies / Технологии бэкенда
- Python 3.14
- Streamlit for web interface
- Pandas for data manipulation
- Plotly for interactive visualizations
- NumPy for numerical computations

### Development Tools / Инструменты разработки
- Pytest for testing
- Flake8 for code linting
- Black for code formatting
- Docker for containerization

## Testing / Тестирование

### Running Tests / Запуск тестов
```bash
# Run all tests
python -m pytest test_analysis.py -v

# Run with coverage
python -m pytest test_analysis.py --cov=disc_cutting_analyzer
```

### Test Coverage / Покрытие тестами
- Unit tests for all analysis functions
- Integration tests for data flow
- Validation tests for user inputs
- Edge case testing for error handling

## Deployment / Развертывание

### GitHub Actions Pipeline / Конвейер GitHub Actions
The project includes an automated CI/CD pipeline that:
1. Runs tests on every push and pull request
2. Builds and deploys Docker image to DockerHub on successful tests
3. Uses `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` for authentication

### Docker Configuration / Конфигурация Docker
- Base image: python:3.14-slim
- Port: 8501 (default Streamlit port)
- Includes health check endpoint
- Optimized for production deployment

### DockerHub Deployment / Развертывание в DockerHub
1. Set up secrets in GitHub repository:
   - `DOCKERHUB_USERNAME`
   - `DOCKERHUB_TOKEN`
2. Push to main branch to trigger deployment
3. Image is tagged as `latest` and with commit SHA

---

## License / Лицензия

This project is licensed under the terms specified in the LICENSE file.

## Contributing / Содействие

Contributions are welcome! Please read the contributing guidelines before submitting pull requests.

## Contact / Контакты

For questions or support, please contact the project maintainers.