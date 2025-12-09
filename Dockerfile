# Use official Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements if exists
COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt || true

# Copy project files
COPY . .

# Default command
CMD ["python3", "demo_great_expectations.py"]
