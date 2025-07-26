import pytest
from flask import Flask, jsonify
from flask.testing import FlaskClient
from app import app
from models import db, Student, Professor, Marks
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

@pytest.fixture
def client():
    """Fixture to create a test client for the Flask app."""
    app.testing = True
    return app.test_client()

def test_home_api(client: FlaskClient):
    """Test the home API (/) to ensure it returns the correct message."""
    response = client.get("/")
    json_data = response.get_json()

    # Print the response for debugging
    print("\nResponse JSON:", json_data)
    assert response.status_code == 200
    assert response.get_json() == {"message": "Welcome to the App"}

def test_register_api(client: FlaskClient):
    """Test the registration API (/api/register) with valid user data."""
    data = {
        "name": "Anil",
        "email": "024@ds.study.iitm.ac.in",
        "password": "Anil",
        "roll_no": "024"
    }

    response = client.post("/api/register", json=data)
    json_data = response.get_json()

    # Print the response for debugging
    print("\nResponse JSON:", json_data)

    assert response.status_code == 201
    assert json_data == {"message": "Student registered successfully"}




def test_register_already_registered_email(client: FlaskClient):
    """Test the registration API when the email is already registered."""
    data = {
        "name": "abhishek",
        "email": "022@ds.study.iitm.ac.in",
        "password": "abhishek",
        "roll_no": "022"
    }

    response = client.post("/api/register", json=data)
    json_data = response.get_json()

    # Print the response for debugging
    print("\nResponse JSON:", json_data)

    assert response.status_code == 400
    assert json_data == {"message": "Email already registered"}


def test_login_api(client: FlaskClient):
    """Test the login API (/api/login) with valid credentials."""
    data = {
        "email": "023@ds.study.iitm.ac.in",
        "password": "Rounak"
    }

    expected_response = {
        "message": "Login successful",
        "student": {
            "name": "Rounak",
            "email": "023@ds.study.iitm.ac.in",
            "roll_no": "023"
        }
    }

    response = client.post("/api/login", json=data)
    json_data = response.get_json()

    print("\nResponse JSON:", json_data)

    assert response.status_code == 200
    assert json_data == expected_response

def test_login_empty_inputs(client):
    data = {
        "email": "",
        "password": ""
    }
    response = client.post("/api/login", json=data)
    assert response.status_code == 400
    assert response.get_json()["message"] == "Email and password are required"


def test_login_invalid_credentials(client: FlaskClient):
    """Test the login API (/api/login) with invalid credentials."""
    data = {
        "email": "023@ds.study.iitm.ac.in",
        "password": "rounak"
    }

    expected_response = {
        "message": "Invalid credentials"
    }

    response = client.post("/api/login", json=data)
    json_data = response.get_json()

    print("\nResponse JSON:", json_data)

    assert response.status_code == 401
    assert json_data == expected_response


def test_search_api(client: FlaskClient):
    """Test the search API (/api/search) with a query."""
    data = {"query": "what is binary search"}
    
    response = client.post("/api/search", json=data)
    json_data = response.get_json()

    # print("\nResponse JSON:", json_data)

    assert response.status_code == 200 # Ensure response contains expected key
    assert len(json_data)>=1# Ensure response contains expected key

def test_search_empty_query(client):
    data = {"query": ""}
    response = client.post("/api/search", json=data)
    assert response.status_code == 400
    assert response.json == {"error": "Query parameter is required"}


def test_codeassist(client):
    """Test the /api/codeassist endpoint with a programming problem and error code."""
    data = {
        "problem_statement": "find the odd number",
        "error_code": "if n%2==0; print('odd number')"
    }

    response = client.post("/api/codeassist", json=data)  # Send POST request

    assert response.status_code == 200  # Ensure HTTP 200 response
    response_json = response.get_json()  # Parse JSON response
    assert isinstance(response_json, dict)  # Ensure response is a dictionary
    assert len(response_json) > 0  

def test_code_assist_empty_inputs(client):
    data = {"problem_statement": "", "error_code": ""}
    response = client.post("/api/codeassist", json=data)
    assert response.status_code == 400
    assert response.json == {"error": "Both problem statement and error code are required"}


def test_codeassist_incomplete_params(client: FlaskClient):
    # Define the incomplete data (missing error_code)
    data = {
        "problem_statement": "find the odd number"
    }

    # Send a POST request to /api/codeassist
    response = client.post("/api/codeassist", json=data)

    # Parse the response
    json_response = response.get_json()

    # Assertions
    assert response.status_code == 400
    assert "error" in json_response
    assert json_response["error"] == "Both problem statement and error code are required"

# def test_support_api(client):
#     # Define the query parameter
#     data = {
#         "query": "how many credits are there in BS level?"
#     }

#     # Send a POST request to /api/support
#     response = client.post("/api/support", json=data)

#     # Parse the response
#     json_response = response.get_json()

#     # Assertions
#     assert response.status_code == 200
#     assert json_response is not None
#     assert len(json_response) > 0

def test_chatai_api(client):
    # Define the query parameter
    data = {
        "query": "what is A* search in AI?"
    }

    # Send a POST request to /api/chatai
    response = client.post("/api/chatai", json=data)

    # Parse the response
    json_response = response.get_json()

    # Assertions
    assert response.status_code == 200
    assert json_response is not None
    assert len(json_response) > 0

def test_study_group_recommendation_api(client):
    # Define the request data
    data = {
        "roll_no": "002"
    }

    # Send a POST request to /api/study-group-recommendation
    response = client.post("/api/study-group-recommendation", json=data)

    # Parse the response
    json_response = response.get_json()

    # Assertions
    assert response.status_code == 200
    assert json_response is not None
    assert len(json_response) > 0

# def test_generate_reports(client):
#     response = client.get('/api/generate-reports')  # Use GET method
#     assert response.status_code == 200
#     data = response.get_json()
#     assert "response" in data
#     assert "html_report_path" in data["response"]
#     assert "pdf_report_path" in data["response"]
#     assert data["response"]["html_report_path"] == "templates/report.html"
#     assert data["response"]["pdf_report_path"] == "templates/report.pdf"

def test_get_students(client):
    response = client.get('/api/students')  # Use GET method
    assert response.status_code == 200
    
    data = response.get_json()
    assert isinstance(data, dict) 
    
def test_get_professors(client):
    response = client.get('/api/professors')  # Use GET method
    assert response.status_code == 200
    
    data = response.get_json()
    assert isinstance(data, dict) 
    
def test_get_marks(client):
    response = client.get('/api/addMarks')  # Use GET method
    assert response.status_code == 200
     # Check if response is a dict