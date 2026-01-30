# GitHub Webhook Receiver

A Flask-based webhook receiver application that captures GitHub events (push, merge, pull requests) and stores them in MongoDB. Includes a real-time Streamlit dashboard for monitoring events.

## Overview

This application acts as a webhook endpoint for GitHub repositories. When configured as a webhook receiver, it captures GitHub events, stores them in a MongoDB database, and provides a visual dashboard to monitor repository activity in real-time.

## Features

- Receives and processes GitHub webhook events
- Supports multiple event types (Push, Merge, Pull Request)
- Stores event data in MongoDB
- Real-time dashboard with auto-refresh
- Visual event feed with color-coded activity cards
- Event metrics and statistics

## Prerequisites

Before setting up this application, ensure you have the following installed:

- Python 3.7 or higher
- MongoDB (local or cloud instance)
- pip (Python package manager)

## Installation

### 1. Clone the Repository

Clone this repository to your local machine.

### 2. Create Virtual Environment

Create a Python virtual environment to isolate project dependencies:

**Windows:**
```
python -m venv .venv
.venv\Scripts\activate
```

**macOS/Linux:**
```
python -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

Install all required Python packages using the requirements file.

### 4. Configure MongoDB Connection

Edit the MongoDB connection string in the application configuration file. You'll need to provide your MongoDB URI (local or cloud MongoDB Atlas connection string).

**Important:** Never commit your actual MongoDB credentials to version control.

## Configuration

### MongoDB Setup

The application requires a MongoDB database connection. Configure the connection string in the Flask app initialization file.

- For local MongoDB: Use a connection string pointing to your local instance
- For MongoDB Atlas: Use the connection string provided by Atlas

### GitHub Webhook Setup

To receive events from GitHub:

1. Go to your GitHub repository settings
2. Navigate to "Webhooks" section
3. Click "Add webhook"
4. Set the Payload URL to your application endpoint (e.g., `http://yourdomain.com/webhook/receiver`)
5. Set Content type to `application/json`
6. Select which events you want to receive (pushes, pull requests, merges)
7. Save the webhook

**Note:** For local development, you may need to use a service like ngrok to expose your local server to the internet.

## Running the Application

### Start the Flask Backend

Run the Flask application which serves as the webhook receiver and API server. The server will start on port 5000 by default.

### Start the Streamlit Dashboard

Run the Streamlit frontend application to view the visual dashboard. The dashboard will open in your browser and automatically refresh every 15 seconds to show new events.

## Project Structure

### Root Files

- **run.py** - Entry point for the Flask application. Contains the main server configuration and test endpoint.

- **requirements.txt** - Lists all Python dependencies required for the project (Flask, Flask-Cors, Flask-Login, Flask-PyMongo, pymongo).

- **.gitignore** - Specifies which files and folders Git should ignore (virtual environments, cache files, environment variables).

### app/ Directory

Main application package containing the Flask backend logic.

- **app/\_\_init\_\_.py** - Flask application factory. Initializes the app, configures MongoDB connection, and registers blueprints.

- **app/extensions.py** - Contains Flask extension instances (PyMongo for MongoDB connectivity).

### app/webhook/ Directory

Webhook handling module.

- **app/webhook/routes.py** - Defines webhook endpoints:
  - `/webhook/receiver` (POST) - Receives GitHub webhook events
  - `/webhook/data` (GET) - Retrieves latest events from database

- **app/webhook/controller.py** - Contains business logic for processing GitHub webhook payloads and extracting relevant data.

- **app/webhook/schema/** - Request schema definitions and data models for webhook payloads.

### ui/ Directory

Frontend dashboard interface.

- **ui/frontend.py** - Streamlit application that displays a real-time feed of GitHub events with:
  - Auto-refreshing event list (15-second interval)
  - Color-coded event cards for different action types
  - Event metrics and statistics
  - Formatted timestamps and branch information

## API Endpoints

### POST /webhook/receiver

Receives GitHub webhook events and stores them in MongoDB.

**Response:** JSON object with status, message, and inserted document ID.

### GET /webhook/data

Retrieves the 10 most recent webhook events from the database.

**Response:** JSON array containing event documents sorted by timestamp (newest first).

## Dashboard Features

The Streamlit dashboard provides:

- **Real-time Updates** - Automatically fetches new events every 15 seconds
- **Event Cards** - Visual cards showing:
  - Event type (Push, Merge, Pull Request)
  - Author name
  - Branch information
  - Timestamp
  - Color-coded indicators
- **Metrics** - Quick statistics showing total events, merge count, and push count
- **Manual Refresh** - Button to manually trigger data refresh

## Event Types Supported

- **PUSH** - Code pushed to a branch
- **MERGE** - Branch merged into another branch
- **PULL_REQUEST** - New pull request opened

## Database Schema

Events are stored in the `github-actions` collection with the following structure:

- Action type (PUSH, MERGE, PULL_REQUEST)
- Author information
- Source branch (from_branch)
- Target branch (to_branch)
- Timestamp
- Additional metadata from GitHub webhook payload

## Development

### Debug Mode

The Flask application runs in debug mode by default for development purposes. For production deployment, disable debug mode.

### Database Connection Testing

The application tests the MongoDB connection on startup and prints connection status to the console.

## Troubleshooting

### MongoDB Connection Issues

- Verify your MongoDB service is running
- Check the connection string format
- Ensure network access is allowed (for MongoDB Atlas, whitelist your IP)

### Webhook Not Receiving Events

- Confirm the webhook URL is accessible from the internet
- Check GitHub webhook delivery history for error messages
- Verify the endpoint URL is correct
- Ensure the Flask server is running

### Dashboard Not Showing Data

- Verify the Flask API is running on port 5000
- Check that events exist in the MongoDB database
- Confirm the API_URL in the Streamlit app matches your Flask server address
