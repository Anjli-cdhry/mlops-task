import argparse
import pandas as pd
import numpy as np
import yaml
import time
import json
import logging
import sys


def load_config(config_path):
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    if config is None:
        raise ValueError("Config file is empty or invalid")
    
    # validation
    required_keys = ["seed", "window", "version"]
    for key in required_keys:
        if key not in config:
            raise ValueError(f"Missing config key: {key}")

    return config


def load_data(input_path):
    try:
        df = pd.read_csv(input_path)
    except Exception:
        raise ValueError("Invalid or missing CSV file")

    if df.empty:
        raise ValueError("CSV is empty")

    if "close" not in df.columns:
        raise ValueError("Missing 'close' column")

    return df


def process(df, window):
    df["rolling_mean"] = df["close"].rolling(window=window).mean()
    df = df.dropna()
    df["signal"] = (df["close"] > df["rolling_mean"]).astype(int)
    return df


def compute_metrics(df, start_time, config):
    rows = len(df)
    signal_rate = df["signal"].mean()
    latency = int((time.time() - start_time) * 1000)

    return {
        "version": config["version"],
        "rows_processed": rows,
        "metric": "signal_rate",
        "value": round(signal_rate, 4),
        "latency_ms": latency,
        "seed": config["seed"],
        "status": "success"
    }


def write_json(output_path, data):
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)


def setup_logger(log_file):
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--log-file", required=True)

    args = parser.parse_args()

    setup_logger(args.log_file)

    start_time = time.time()

    try:
        logging.info("Job started")

        config = load_config(args.config)
        np.random.seed(config["seed"])
        logging.info(f"Config loaded successfully: seed={config['seed']}, window={config['window']}, version={config['version']}")
        df = load_data(args.input)
        logging.info(f"Dataset loaded with {len(df)} rows")

        
        logging.info("Starting rolling mean calculation")
        df = process(df, config["window"])
        logging.info("Signal generation completed")
        metrics = compute_metrics(df, start_time, config)

        write_json(args.output, metrics)

        logging.info(f"Final metrics: {metrics}")
        logging.info("Job completed successfully")

        print(json.dumps(metrics, indent=2))

    except Exception as e:
        error_output = {
            "version": "v1",
            "status": "error",
            "error_message": str(e)
        }

        write_json(args.output, error_output)

        logging.error(str(e))
        print(json.dumps(error_output, indent=2))

        sys.exit(1)


if __name__ == "__main__":
    main()