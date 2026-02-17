# Technology Stack & Concepts

## Core Components

### 1. ELK Stack (Elasticsearch, Logstash, Kibana)
-   **Elasticsearch**: A distributed, RESTful search and analytics engine. Used here as the primary database for storing logs.
-   **Logstash**: A server-side data processing pipeline that ingests data from multiple sources simultaneously, transforms it, and then sends it to a "stash" like Elasticsearch.
-   **Kibana**: Visualize data with charts and graphs in Elasticsearch. Used for the dashboard.

### 2. Machine Learning
-   **Isolation Forest**: An unsupervised learning algorithm for anomaly detection. It works by isolating observations by randomly selecting a feature and then randomly selecting a split value between the maximum and minimum values of the selected feature.
    -   *Why it works*: Anomalies are few and different. They are easier to isolate (require fewer splits) than normal points.
-   **Scikit-learn**: Python library used to implement Isolation Forest.

### 3. Containerization
-   **Docker**: Used to package the application and its dependencies into a container.
-   **Docker Compose**: A tool for defining and running multi-container Docker applications.

## Project Structure
-   `log-generator/`: Simulates network trafficlogs.
-   `ml-detection/`: The "brain" of the system. Reads from ES, detects anomalies, writes back to ES.
-   `elk-config/`: Configuration files for the stack.
