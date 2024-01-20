# Use an official Python runtime as a parent image
FROM python:3.9.13

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8010 available to the world outside this container
EXPOSE 5050

# Run app.py when the container launches
ENV FLASK_APP main.py

# Run app.py when the container launches
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5050", "--timeout", "800", "app:app"]
