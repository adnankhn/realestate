# Base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Gunicorn
RUN pip install gunicorn

# Copy the application code
COPY . .

# Expose the application port
EXPOSE 8000

# Run migrations and start the Gunicorn server
CMD ["sh", "-c", "python manage.py migrate && gunicorn realestate.wsgi:application --workers 4 --bind 0.0.0.0:8000"]
