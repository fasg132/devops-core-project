# Use an official, lightweight Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Set environment variables to prevent Python from writing .pyc files and buffering stdout/stderr
ENV PYTHONTONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy only the requirements file first to leverage Docker cache layering
COPY requirements.txt .

# Install application dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY app.py .

# CyberSec Best Practice: Create a non-root user and switch to it
# Running as root inside a container is a security risk
RUN useradd -u 8888 appuser && chown -R appuser:appuser /app
USER appuser

# Expose the port the Flask app runs on
EXPOSE 5000

# Define the command to run the application
CMD ["python", "app.py"]