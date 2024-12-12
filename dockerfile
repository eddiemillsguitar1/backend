# Use the official Python image
FROM python:3.8-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt /app/

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install system dependencies for Spleeter (ffmpeg)
RUN apt-get update && apt-get install -y ffmpeg

# Copy the application code to the container
COPY . /app/

# Expose the port the app runs on
EXPOSE 5000

# Start the Flask app
CMD ["python", "app.py"]
