# Use official Python image
FROM python:3.10

# Set working directory in container
WORKDIR /app

# Copy the project files to the container
COPY . /app/

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose port 8000 (default Django port)
EXPOSE 8000

# Command to run the Django application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

