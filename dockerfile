# Use the official lightweight Python image
FROM python:3.10-slim

# Set the timezone explicitly to UTC
ENV TZ=Etc/UTC

# Set the working directory inside the container
WORKDIR /app

# Copy requirements
COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Specify the command that will be executed when the container starts
CMD ["python", "main.py"]
