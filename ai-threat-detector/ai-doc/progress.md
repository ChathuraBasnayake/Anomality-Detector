# Implementation Progress

## Phase 1: Ingestion & Storage
-   **Infrastructure**: Docker Compose setup for Elasticsearch, Logstash, Kibana (7.17.9).
-   **Configuration**:
    -   `logstash.conf`: Configured TCP input on port 5000 and output to Elasticsearch.
    -   `kibana.yml`: Configured connection to Elasticsearch.

## Phase 2: ML Detection (In Progress)
-   **Service**: Python service using `scikit-learn` and `elasticsearch`.
-   **Logic Implemented**:
    -   `fetch_data`: Retrieves logs from the last N minutes.
    -   `preprocess_data`: Extracts `bytes_sent` and encodes `status`/`action`.
    -   `train_model`: Uses Isolation Forest for unsupervised anomaly detection.
    -   `detect_anomalies`: Flags potential threats.

## Next Steps
-   Wait for Docker images to download.
-   Verify end-to-end data flow (Log Generator -> Logstash -> ES -> ML -> ES).
-   Set up Kibana visualizations.
