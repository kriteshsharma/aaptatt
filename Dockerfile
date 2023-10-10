# Use a small base image
FROM python:3.9-slim-buster

# Set the working directory inside the container
WORKDIR /app

# Copy the local requirements.txt file to the container
COPY requirements.txt .

# Install the Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code to the container
COPY . .

# Expose the port your Flask app will run on
EXPOSE 5000

# Define the command to run your Flask app
CMD ["python", "app.py"]
