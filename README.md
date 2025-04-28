# OpenAI Image Analyzer Web App

A simple web application that allows users to upload an image and receive an analysis using OpenAI's \`o4-mini\` vision model. Built with FastAPI and Python for the backend API, served by Nginx, and managed with Gunicorn and Systemd on an Ubuntu server.

## Features

*   User-friendly web interface to upload images (JPEG, PNG, WEBP, GIF).
*   Image analysis powered by the OpenAI \`o4-mini\` model.
*   Static frontend files (HTML, CSS, JS) served efficiently by Nginx.
*   Asynchronous FastAPI backend for handling image processing and API calls.

## Tech Stack

*   **Backend:** Python, FastAPI
*   **AI Model:** OpenAI API (`o4-mini`)
*   **Frontend:** HTML, CSS, JavaScript
*   **Web Server / Reverse Proxy:** Nginx
*   **WSGI/ASGI Server:** Gunicorn
*   **Process Manager:** Systemd
*   **Database:** None (stateless)
*   **Deployment:** Ubuntu Server

## Prerequisites

Before you begin, ensure you have the following:

*   An Ubuntu Server (e.g., DigitalOcean Droplet, AWS EC2, physical server).
*   SSH access to the server with `sudo` privileges.
*   A non-root user configured for running the application (recommended).
*   Python 3.x and `pip` installed.
*   Nginx installed.
*   An OpenAI API Key.
*   Git installed (for cloning the repository).
*   Firewall configured to allow HTTP (port 80) and SSH traffic.

## Setup Instructions

Follow these steps on your Ubuntu server:

**1. Clone the Repository**

```bash
git clone https://github.com/netizen488/OpenAI-Image-Analyzer.git
cd https://github.com/netizen488/OpenAI-Image-Analyzer.git
```

**2. Backend Setup**

*   **Create & Activate Virtual Environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
*   **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
*   **Configure OpenAI API Key:**
    Copy the example environment file and edit it to add your key:
    ```bash
    nano .env # Add OPENAI_API_KEY=your_key
    ```

**3. Frontend Setup (Static Files)**

*   **Create Nginx web root:**
    ```bash
    sudo mkdir -p /var/www/html
    ```
*   **Copy Static Files:**
    ```bash
    sudo cp -r static/* /var/www/html/
    ```
*   **Set Permissions:**
    ```bash
    sudo chown -R www-data:www-data /var/www/html
    sudo chmod -R 755 /var/www/html
    ```

**4. Nginx Configuration**

*   **Copy Nginx Config:**
    Use the provided `nginx.nginx` template.
    ```bash
    sudo cp nginx.nginx /etc/nginx/sites-available/default
    ```
*   **Edit Nginx Config:**
    Update `server_name` with your server's IP or domain.
    ```bash
    sudo nano /etc/nginx/sites-available/default
    ```
*   
*   **Test & Restart Nginx:**
    ```bash
    sudo nginx -t
    sudo systemctl restart nginx
    ```

## Running the Application

    ```bash
    uvicorn main:app --host 127.0.0.1 --port 8000 --reload
    ```

## Project Structure

```
.
├── .env.example      # Example environment file
├── .gitignore
├── main.py           # FastAPI application
├── nginx/
│   └── image_analyzer.nginx # Nginx config template
├── requirements.txt  # Python dependencies
├── static/           # Frontend files
│   ├── index.html
│   ├── script.js
│   └── style.css
├── systemd/
│   └── image_analyzer.service # Systemd service template
└── README.md