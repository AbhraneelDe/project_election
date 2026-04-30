# Use the official lightweight Python image.
FROM python:3.11-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy local code to the container image
COPY . .

# Run collectstatic to prepare static files for production
RUN python manage.py collectstatic --noinput

# Run the web service on container startup using Gunicorn.
# Cloud Run expects the server to listen on the port defined by the $PORT environment variable.
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 election_assistant.wsgi:application
