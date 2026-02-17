# Visualize Your Threats (Kibana)

Since Kibana dashboards are created via the UI, here is how you build the "Threat Map":

## 1. Access Kibana
-   Open your browser and got to: `http://localhost:5601`
-   Wait for it to load (it might take a minute).

## 2. Connect Data (Index Pattern)
1.  Go to **Stack Management** > **Index Patterns**.
2.  Click **Create index pattern**.
3.  Name: `network-logs-*`
4.  Timestamp field: `timestamp`
5.  Click **Create index pattern**.

## 3. Create Dashboard
1.  Go to **Dashboard** in the sidebar.
2.  Click **Create dashboard**.
3.  **Add Visualization** > **Lens**:
    -   **Metric**: Drag `Count` of records.
    -   **Filter**: Add filter `is_anomaly : -1`. This shows "Total Threats detected".
4.  **Add Visualization** > **Table**:
    -   Rows: `ip_address`, `action`, `bytes_sent`.
    -   Sort by: `@timestamp` descending.
    -   Filter: `is_anomaly : -1`.
    -   Title: "Live Threat Feed".
5.  **Save Dashboard**: Name it "Cybersecurity Threat Center".

## 4. Test It
-   The default logs are mostly normal.
-   Wait a few minutes. The `log-generator` occasionally sends a "SUDO_ACCESS" failure.
-   You should see these appear in your "Live Threat Feed" automatically!
