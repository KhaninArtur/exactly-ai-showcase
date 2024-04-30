# CatDog🐾 Image Gallery Backend

This document provides setup and operational details for the backend of the CatDog🐾 Image Gallery, a dynamic web application that displays categorized images of cats and dogs. 

Built with FastAPI, the backend orchestrates image fetching, classification, and storage, leveraging cloud resources for efficiency and scalability.

## Quick Start

```bash
# Install dependencies
poetry install

# Start the development server
uvicorn main:app --reload
```

Ensure the [environment variables](#environment-variables) are configured in your `.env` file.

## Environment Variables

The backend application uses several environment variables to configure its operation. Set these variables in your `.env` file to match your specific deployment environment:

- `DEBUG`: Set to `True` to enable debug mode, which provides detailed error logs and runtime information. Use `False` for production environments to enhance performance and security.
- `LOCAL`: Set to `True` to run the application in a local development environment. This configures CORS to allow all requests from the local frontend server.
- `IMAGES_LIMIT`: Defines the maximum number of images per category (cat/dog) to fetch in one API call.
- `DATABASE_URL`: Connection string for the database.
- `EXACTLY_API`: URL for the external API from which the application retrieves generated image data.
- `GCS_SERVICE_ACCOUNT_KEY_BASE64`: Base64-encoded Google Cloud Service account key required for accessing Google Cloud Storage. Ensure this key has appropriate permissions for the operations your backend will perform.
- `GS_BUCKET_NAME`: Name of the Google Cloud Storage bucket where images are stored. This should match the bucket name configured in your Google Cloud Storage.

When deploying into production or using Docker, add the following environment variables to serve the frontend.
- `PUBLIC_STORAGE_BASE_URL`: Base URL for accessing the stored images. This URL is used to construct accessible paths to the images stored in Google Cloud Storage.
- `PUBLIC_API_URL`: URL where your public API is accessible. This is used internally to configure service endpoints and by the frontend to make API requests.

## Architecture Overview

- **API** ([`/api`](api)): Defines the routes and endpoints.
- **Internal** ([`/internal`](internal)): Core logic including database interactions, services, and utilities.
- **Entry Point** ([`main.py`](main.py)): Configures and launches the FastAPI application.

## Features

- **Continuous Data Fetching**: Asynchronously fetches and processes images in real-time, ensuring fresh content availability.
- **Image Classification**: Automatically classifies each fetched image as either a cat or a dog using advanced machine learning models.
- **Retrieving the Latest Images**: Provides the most recent images to users.
- **Cloud Storage**: Utilizes Google Cloud Storage for reliable and scalable image data management.


## Running Locally

For development, the server can be run with hot reload enabled to facilitate rapid iteration:

```bash
uvicorn main:app --reload
```

CORS is configured for local development to allow interactions from the frontend running at http://localhost:5173.

## Deployment
The application is container-ready with Docker, suitable for deployment on any platform that supports Docker containers:

```bash
docker build -t catdog .
docker run -p 80:8000 catdog
```

## Further Documentation

For more detailed API usage and backend functionality, refer to the generated FastAPI documentation accessible through the /docs route when running the server.