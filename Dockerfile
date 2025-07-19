# Use official Python image
FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Copy all project files to /app in the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Start the app (NOT with gunicorn, just Python)
CMD ["python", "app.py"]
