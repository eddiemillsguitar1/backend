# Use an official Python image as a base
FROM python:3.8-slim

# Set environment variables to prevent interactive prompts during installation
ENV DEBIAN_FRONTEND=noninteractive

# Install necessary system dependencies (including ffmpeg and git)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install the dependencies (installing chord-detection separately)
RUN pip install --no-cache-dir -r requirements.txt

# Clone chord-detection manually from GitHub
RUN git clone https://github.com/belovm96/chord-detection.git && cd chord-detection && pip install .

# Copy the rest of the application code into the container
COPY . /app/

# Expose the port that Flask will run on
EXPOSE 5000

# Set the command to run the app
CMD ["python", "app.py"]
