FROM python:3.9-slim

WORKDIR /app

# Install dependencies
RUN pip install faker requests

# Copy script
COPY generate_logs.py .

CMD ["python", "generate_logs.py"]
