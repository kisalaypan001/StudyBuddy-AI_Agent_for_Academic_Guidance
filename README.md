# STUDYBUDDY-AI-AGENT-FOR-ACADEMIC-GUIDANCE-

#  Project Setup Guide

This guide provides step-by-step instructions to set up and run the backend and frontend of the project.

## Technology Stack

- Backend Python, Flask
- Frontend JavaScript, Vue js
- Database SQLite
- Package Management pip (Python), npm (Node.js)
- Version Control Git

## Prerequisites

Before you begin, ensure you have the following installed on your system

- Python (version 3.x)
- Node.js (with npm)


## Getting Started

Follow these steps to set up and run the project.

### 1. Setting Up the Backend

1. Open Terminal Navigate to the project directory and then to the backend folder.

    ```bash
    cd backend
    ```

2. Create a Virtual Environment Run the following command to create a virtual environment.

    ```bash
    python3 -m venv env_name
    ```

3. Activate the Virtual Environment Activate the virtual environment using the following command.

    - On macOSLinux

        ```bash
        source env_namebinactivate
        ```

    - On Windows (use Command Prompt)

        ```cmd
        env_nameScriptsactivate
        ```

4. Install Dependencies Install the necessary Python packages by running

    ```bash
    pip install -r requirements.txt
    ```

5. Run the Python App Start the backend server.

    ```bash
    python3 app.py
    ```

- Once the backend is compiled and running, access the backend at

    ```url
    httplocalhost5000
    ```

### 2. Setting Up the Frontend


1. Setup the Project Keep the backend running, and in a new terminal tab, Navigate to the frontend folder then to the my-vue-spa folder.

    ```bash
    cd frontendmy-vue-spa
    ```

2. Setup the Project Install the necessary Node.js packages.

    ```bash
    npm install
    ```

3. Compile the Frontend Start the frontend server.

    ```bash
    vue run serve
    ```

### 3. Access the Application

- Once the frontend is compiled and running, access the application by opening a web browser and navigating to

    ```url
    httplocalhost8080
    ```

## Additional Notes

- Ensure the backend server is running before starting the frontend.
- Any changes to the frontend code will automatically recompile and refresh the browser.
