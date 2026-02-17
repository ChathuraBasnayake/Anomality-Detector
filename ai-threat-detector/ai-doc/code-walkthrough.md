# Code Walkthrough

This document explains the core files implemented in the project so far.

## 1. System Orchestration: `docker-compose.yml`
This file defines the entire infrastructure. It spins up 5 containers:
-   **`elasticsearch`**: The database that stores all logs.
-   **`logstash`**: Receives logs from the generator, processes them, and sends them to Elasticsearch.
-   **`kibana`**: The web dashboard (port 5601) to visualize the data.
-   **`log-generator`**: A custom Python container that runs our log generation script.
-   **`ml-detection`**: A custom Python container that runs our anomaly detection logic.

**Key Definition**:
```yaml
ml-detection:
  build: ./ml-detection  # Builds from the Dockerfile in ml-detection/ folder
  environment:
    - ELASTICSEARCH_HOST=elasticsearch # Sets env var so code knows where ES is
```

## 2. Data Source: `log-generator/generate_logs.py`
This script simulates a busy network.
-   **`generate_log_entry()`**: Creates a dictionary with fake data (IP, User, Action). It purposefully injects an anomaly (SUDO_ACCESS failure) 5% of the time.
-   **`send_logs()`**: Connects to Logstash via TCP on port 5000 and streams the logs line-by-line as JSON.

**Snippet**:
```python
# Simulate an anomaly occasionally
if random.random() < 0.05:
    log_entry["action"] = "SUDO_ACCESS"
    log_entry["status"] = "FAILURE"
```

## 3. Data Pipeline: `elk-config/logstash/pipeline/logstash.conf`
This tells Logstash how to handle the data.
-   **Input**: Listens on TCP port 5000.
-   **Output**: Sends data to Elasticsearch index `network-logs-YYYY.MM.dd`.

## 4. The Brain: `ml-detection/detector.py`
This is the core ML logic.
-   **`fetch_data()`**: Queries Elasticsearch for the last N minutes of logs.
-   **`preprocess_data()`**: Converts raw logs into numbers for the model.
    -   Encodes `FAILURE` as 1, `SUCCESS` as 0.
    -   Encodes `SUDO_ACCESS` as 1, others as 0.
-   **`train_model()`**: Uses **Isolation Forest** (Unsupervised Learning). It doesn't need labeled data; it just learns "what is normal" and flags outliers.
-   **`main()` loop**: Runs every minute to fetch new data, retrain/predict, and log anomalies.

**Key Logic**:
```python
# -1 means anomaly, 1 means normal
df['is_anomaly'] = model.predict(X) 
anomalies = df[df['is_anomaly'] == -1]
```
