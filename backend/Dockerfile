# Dockerfile for the FastAPI backend

# Use the official Python image as the base image
FROM python:3.11.4-alpine

# Set the working directory in the container
WORKDIR /backend/app

# Copy the backend files to the container's working directory
COPY requirements.txt .

# Install the backend dependencies
RUN apk add --update --no-cache gcc g++ python3-dev libpq-dev && \
    pip install -r requirements.txt && \
    adduser -D app_user

COPY __init__.py /backend/
COPY ./app /backend/app

# Expose the port used by the FastAPI server
EXPOSE 8000

USER app_user

# Start the FastAPI server
CMD [ "gunicorn", "main:app" ,"-k", "uvicorn.workers.UvicornWorker", \
      "--bind", "0.0.0.0:8000", "--workers", "1", "--timeout", "3600" ]
