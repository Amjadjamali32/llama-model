# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy .env file (if exists) into the container
COPY .env /app/.env

# Set environment variables for Flask app
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Expose port 5000 for Flask
EXPOSE 5000

# Run the Flask app
CMD ["flask", "run"]
