# Use an official Node.js runtime as a parent image for building the frontend
FROM node:20-alpine as build-stage

# Set working directory
WORKDIR /app/frontend

# Copy package.json and other relevant files
COPY frontend/package*.json ./

# Install dependencies
RUN npm install

# Copy frontend source code
COPY frontend/ .

# Build static files
RUN npm run build

# Use an official Python runtime to build and run the backend
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install poetry
ENV POETRY_VERSION=1.8.2
RUN pip install "poetry==$POETRY_VERSION"

# Copy only the files needed for poetry to install dependencies
COPY backend/pyproject.toml backend/poetry.lock* ./

# Configure poetry and install dependencies
RUN poetry config virtualenvs.create false \
  && poetry install --no-dev --no-interaction --no-ansi

# Copy the backend source code
COPY backend/ .

# Copy the built frontend into the correct location for FastAPI to serve
COPY --from=build-stage /app/frontend/build /app/frontend

# Expose port
EXPOSE 8000

# Define the volume
VOLUME /app/database

# Run the application
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]