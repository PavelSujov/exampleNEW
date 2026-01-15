# Docker Deployment Guide

## Prerequisites

Before building and running the Docker container, ensure you have Docker installed on your system:

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) for Windows/Mac
- [Docker Engine](https://docs.docker.com/engine/install/) for Linux

## Building and Running the Application

### Method 1: Using Docker Compose (Recommended)

1. Navigate to the project directory:
   ```bash
   cd exampleNEW
   ```

2. Build and run the container:
   ```bash
   docker-compose up --build
   ```

3. Access the application at: http://localhost:8501

### Method 2: Using Docker Commands

1. Navigate to the project directory:
   ```bash
   cd exampleNEW
   ```

2. Build the Docker image:
   ```bash
   docker build -t streamlit-disc-analysis-app .
   ```

3. Run the container:
   ```bash
   docker run -p 8501:8501 streamlit-disc-analysis-app
   ```

4. Access the application at: http://localhost:8501

## Dockerfile Explanation

The Dockerfile performs the following steps:

1. Uses Python 3.14 slim image as base
2. Sets working directory to `/app`
3. Copies and installs Python requirements
4. Copies application files
5. Exposes port 8501 (default Streamlit port)
6. Runs the Streamlit application

## Docker Compose Configuration

The docker-compose.yml file defines:

- A service named `streamlit-app`
- Automatic build from the current directory
- Port mapping from host 8501 to container 8501
- Volume mounting for data persistence
- Restart policy to ensure uptime

## Environment Variables

The application can be configured using environment variables:

- `STREAMLIT_SERVER_PORT`: Port to run the Streamlit server (default: 8501)
- `STREAMLIT_SERVER_HEADLESS`: Run in headless mode (default: true)

## Troubleshooting

### Common Issues:

1. **Port Already in Use**: Ensure port 8501 is not being used by another application
2. **Build Errors**: Verify that requirements.txt is properly formatted
3. **Permission Errors**: On Linux/Mac, you may need to run with `sudo`

### Health Check

The container includes a health check endpoint that verifies the Streamlit server is responding.

## Production Deployment

For production deployments, consider:

- Using a reverse proxy (nginx) for SSL termination
- Adding monitoring and logging
- Implementing proper authentication
- Setting up a persistent volume for data storage
- Configuring resource limits and scaling policies