# MLOps Task - Rolling Mean Signal

## Overview
This project implements a minimal MLOps-style batch job in Python.

It processes time-series data using a rolling mean strategy and generates binary trading signals, while demonstrating core MLOps principles such as reproducibility, observability, and deployment readiness.

---

## Key MLOps Concepts Demonstrated

- **Reproducibility**  
  Controlled via `config.yaml` and deterministic execution using a fixed random seed.

- **Observability**  
  Structured logging (`run.log`) and machine-readable metrics (`metrics.json`) for monitoring and debugging.

- **Deployment Readiness**  
  Fully Dockerized pipeline enabling consistent execution across environments with a single command.

---

## Features

- Loads configuration from YAML (`config.yaml`)
- Reads CSV dataset (`data.csv`)
- Validates input data and configuration
- Computes rolling mean on `close` column
- Handles initial NaN values using `dropna()`
- Generates binary signals:
  - 1 if close > rolling mean  
  - 0 otherwise
- Computes performance metrics:
  - rows_processed
  - signal_rate
  - latency_ms
- Outputs:
  - `metrics.json` (structured metrics)
  - `run.log` (detailed logs)
- Graceful error handling:
  - Missing file
  - Invalid CSV
  - Missing columns
  - Invalid config
- Fully Dockerized for reproducible execution

---

## CLI Usage

python run.py --input data.csv --config config.yaml --output metrics.json --log-file run.log

---

## Run Locally

python run.py --input data.csv --config config.yaml --output metrics.json --log-file run.log

---

## Run with Docker

### Build Image
docker build -t mlops-task .

### Run Container
docker run --rm mlops-task

The container:
- Executes the pipeline
- Generates metrics.json and run.log
- Prints final metrics JSON to stdout

---

## Example Output

{
  "version": "v1",
  "rows_processed": 6,
  "metric": "signal_rate",
  "value": 1.0,
  "latency_ms": 8,
  "seed": 42,
  "status": "success"
}

---

## Project Structure

mlops-task/
├── run.py
├── config.yaml
├── data.csv
├── requirements.txt
├── Dockerfile
├── README.md
├── metrics.json
├── run.log

---

## Notes

- Rolling mean introduces NaN values for initial rows, which are handled using dropna() to ensure clean signal generation.
- The system is designed to be deterministic and reproducible across runs.
- Docker ensures environment consistency and ease of deployment.

---

## Submission

This repository includes:
- Complete implementation (run.py)
- Configuration and dataset
- Logs and metrics output
- Dockerized setup
- Documentation (README)