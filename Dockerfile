# Use an official Python runtime as a parent image
FROM python:3.9.13

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app
COPY certificate.pem /path/in/container/certificate.pem
COPY private.pem /path/in/container/private.pem
# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make port 8010 available to the world outside this container
EXPOSE 5050

# Run app.py when the container launches
ENV FLASK_APP app.py

# Run app.py when the container launches
CMD ["gunicorn", "-w", "1", "-t", "2", "-b", "0.0.0.0:5050", "--timeout", "800", "app:app","--max-requests", "10", "--max-requests-jitter", "2"]
