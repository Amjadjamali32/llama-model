# Use a lightweight Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the app files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download SpaCy model
RUN python -m spacy download en_core_web_sm

# Expose the Flask port
EXPOSE 5000

# Run the app
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
