# AI381 Lab 2 – Churn Prediction API

[![AI381 CI Pipeline](https://github.com/tala271/ai381-lab2-churn-api/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/tala271/ai381-lab2-churn-api/actions/workflows/ci.yml)

## Project Overview

This project implements a machine learning churn prediction API using FastAPI. It packages the trained model in Docker and uses GitHub Actions for automated testing, security scanning, and image publishing.

## Technologies

- Python 3.13
- FastAPI
- Scikit-learn
- Docker
- GitHub Actions
- Trivy
- GitHub Container Registry (GHCR)

## Project Structure

.
├── data/
├── models/
├── src/
├── tests/
├── Dockerfile
├── requirements.txt
└── README.md

## API Endpoints

### Health Check

GET /health

Returns the API health status.

### Prediction

POST /predict

Receives customer information and returns a churn prediction with its probability.

## Run Locally

Install dependencies:

pip install -r requirements.txt

Start the API:

uvicorn src.app.main:app --host 0.0.0.0 --port 8000

Open API documentation:

http://localhost:8000/docs

## Run with Docker

Build the Docker image and start the API with one command:

```bash
docker build -t churn-api . && docker run -d -p 8000:8000 --name churn-api churn-api
```

Test the health endpoint:

http://localhost:8000/health


## Testing

The project includes automated tests for:

- API health response.
- Model loading.
- Input validation.
- Unknown categorical values.
- Deterministic predictions.

## CI/CD Pipeline

GitHub Actions automatically:

1. Runs linting and automated tests.
2. Builds the Docker image.
3. Scans the image for HIGH and CRITICAL vulnerabilities using Trivy.
4. Pushes the image to GitHub Container Registry after successful checks on the main branch.

## Docker Image

ghcr.io/tala271/ai381-lab2-churn-api:dcd7deb98edfa2d769ec987979f2eab2673940e0

## Security

The Docker image is scanned using Trivy.

## Author

Tala

AI381 – Machine Learning Operations  
Lab 2
