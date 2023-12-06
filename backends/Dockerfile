# Use the official Python image
FROM python:3.8.5-slim-buster

# Set the working directory
WORKDIR /usr/src/app

# Set environment variables to prevent Python from writing pyc files and buffering output
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copy the local code to the container
COPY . /usr/src/app/

# Upgrade pip and install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt