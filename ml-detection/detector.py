import time
import os
import json
from elasticsearch import Elasticsearch
from sklearn.ensemble import IsolationForest
import pandas as pd
import numpy as np
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Connect to Elasticsearch
es = Elasticsearch([{'host': os.environ.get('ELASTICSEARCH_HOST', 'elasticsearch'), 'port': int(os.environ.get('ELASTICSEARCH_PORT', 9200))}])

def fetch_data(window_minutes=10):
    """
    Fetch logs from the last `window_minutes` from Elasticsearch.
    """
    logger.info("Fetching data from Elasticsearch...")
    query = {
        "query": {
            "range": {
                "@timestamp": {
                    "gte": f"now-{window_minutes}m",
                    "lt": "now"
                }
            }
        },
        "size": 10000 
    }
    
    try:
        res = es.search(index="network-logs-*", body=query)
        hits = res['hits']['hits']
        data = []
        for hit in hits:
            source = hit['_source']
            source['_id'] = hit['_id']
            source['_index'] = hit['_index']
            data.append(source)
        return pd.DataFrame(data)
    except Exception as e:
        logger.error(f"Error fetching data: {e}")
        return pd.DataFrame()

def preprocess_data(df):
    """
    Extract features for the model.
    Focus on numerical features: bytes_sent.
    Encode categorical features: action, status.
    """
    if df.empty:
        return pd.DataFrame()
    
    # Feature Engineering
    features = pd.DataFrame()
    features['bytes_sent'] = df['bytes_sent'].astype(float)
    
    # One-hot encoding for categorical fields (simplified for demo)
    # In a real scenario, use a consistent encoder across train/predict
    # Here we just map known values for simplicity or use frequency encoding
    features['status_code'] = df['status'].apply(lambda x: 1 if x == 'FAILURE' else 0)
    features['action_code'] = df['action'].apply(lambda x: 1 if x == 'SUDO_ACCESS' else 0)
    
    return features.fillna(0) # Handle missing values

def train_model(df):
    """
    Train Isolation Forest model.
    """
    logger.info(f"Training model on {len(df)} records...")
    X = preprocess_data(df)
    if X.empty:
        return None
        
    clf = IsolationForest(contamination=0.01, random_state=42)
    clf.fit(X)
    return clf

def main():
    logger.info("ML Detection Service Started...")
    model = None
    
    # Wait for ES to be up
    time.sleep(30) 

    while True:
        try:
            # 1. Fetch Data
            df = fetch_data(window_minutes=5)
            
            if not df.empty:
                # 2. Train Model (In real app, load pre-trained, but here we train on recent data)
                model = train_model(df)
                
                # 3. Detect Anomalies (Predict on same data for demo purposes)
                if model:
                    X = preprocess_data(df)
                    df['anomaly_score'] = model.decision_function(X)
                    df['is_anomaly'] = model.predict(X) # -1 for anomaly, 1 for normal
                    
                    # Log anomalies
                    anomalies = df[df['is_anomaly'] == -1]
                    if not anomalies.empty:
                        logger.warning(f"⚠️  ALERT: Detected {len(anomalies)} anomalies!")
                        for i, row in anomalies.iterrows():
                            logger.error(f"🚨  THREAT DETECTED: IP={row['ip_address']}, Action={row['action']}, Bytes={row['bytes_sent']}")
                            
                            # Write back to ES
                            try:
                                es.update(index=row['_index'], id=row['_id'], body={"doc": {"anomaly_score": row['anomaly_score'], "is_anomaly": int(row['is_anomaly'])}})
                                logger.info(f"Updated document {row['_id']} with anomaly score.")
                            except Exception as e:
                                logger.error(f"Error updating anomaly log: {e}")
            
            time.sleep(60) 
        except Exception as e:
            logger.error(f"Error in main loop: {e}")
            time.sleep(10)

if __name__ == "__main__":
    main()
