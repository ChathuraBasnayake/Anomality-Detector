FROM python:3.9-slim

WORKDIR /app

# Install dependencies (including sci-kit learn which needs build tools sometimes, but wheel should be fine)
RUN pip install "elasticsearch<8.0.0" scikit-learn pandas joblib

# Copy script
COPY detector.py .

CMD ["python", "detector.py"]
