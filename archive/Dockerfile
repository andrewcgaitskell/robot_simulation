# Use official Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Create app directory
WORKDIR /app

# Copy only requirements first (to leverage Docker cache)
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the rest of the code
COPY . .

# Expose the default Quart port
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]
