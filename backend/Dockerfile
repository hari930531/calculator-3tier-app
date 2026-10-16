# Use a lightweight official Python 3.10 slim runtime
FROM python:3.10-slim

# Set the active working directory inside the container
WORKDIR /app

# Copy dependency definitions first to leverage Docker layer caching
COPY requirements.txt .

# Install all Python dependencies without caching wheels to keep the image compact
RUN pip install --no-cache-dir -r requirements.txt

# Copy all backend application source files into the container working directory
COPY . .

# Expose the Flask/FastAPI backend HTTP listener port
EXPOSE 5000

# Run the backend web application when the container starts
CMD ["python", "app.py"]