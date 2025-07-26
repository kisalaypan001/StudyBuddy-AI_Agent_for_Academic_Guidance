# Home API Tests

**Description:** These APIs have functionality which redirects the user to home page by showing the welcome message.

### Endpoint:

- **URL:** `http://127.0.0.1:5000/api/`  
- **Method:** GET

##### Test Cases:

1. `test_home_api()` Redirects the user to the home page
     
   - Passed Inputs:  
     - `\`  
   - Expected Output:  
     - `HTTP-Status Code: 200`
     -`"message": "Welcome to the App"`  
   - Actual Output:  
     - `HTTP-Status Code: 200`  
     - `"message": "Welcome to the App"`  
   - Result:  
     - `Passed`  
   - Pytest Code:

```
def test_home_api(client: FlaskClient):
    """Test the home API (/) to ensure it returns the correct message."""
    response = client.get("/")
    json_data = response.get_json()

    # Print the response for debugging
    print("\nResponse JSON:", json_data)
    assert response.status_code == 200
    assert response.get_json() == {"message": "Welcome to the App"}
```

# User Registration Tests

**Description:** These APIs have functionality which provides the registration and login functionality to new users.

### Endpoint:

- **URL:** `http://127.0.0.1:5000/api/regsiter`  
- **Method:** POST

##### Test Cases:

2. `test_register_api()` Tests the successful registration of a user with 200 status code 
     
   - Passed Inputs:  
     - ```data = {
        "name": "Anil",
        "email": "024@ds.study.iitm.ac.in",
        "password": "Anil",
        "roll_no": "024"
      }``` 
   - Expected Output:  
     - `HTTP-Status Code: 201`
     -`"message": "Student registered successfully"`  
   - Actual Output:  
     - `HTTP-Status Code: 201`
     - `"message": "Student registered successfully"`  
   - Result:  
     - `Passed`  
   - Pytest Code:

```
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
```

### Endpoint:

- **URL:** `http://127.0.0.1:5000/api/students`  
- **Method:** GET  
1. `test_get_users_successful()` Tests the retrieval of all the students  
   - Passed Inputs:  
     -    
   - Expected Output:  
     - A List of all the users present in the database  
     - `HTTP-Status Code: 200`  
     - `JSON List of all users present`  
   - Actual Output:  
     - `HTTP-Status Code:200`  
     - List of all the users in the database  
   - Result:  
     - `Passed`  
   - Pytest Code:

```
def test_get_students(client):
    response = client.get('/api/students')  # Use GET method
    assert response.status_code == 200
    
    data = response.get_json()
    assert isinstance(data, dict) 
```

### Endpoint:

- **URL:** `http://127.0.0.1:5000/api/register`  
- **Method:** POST  
    
1. `def test_register_already_registered_email()` Tests whether the application correctly rejects invalid or empty inputs during user registration  
     
   - Passed Inputs:  
     - 

```
{
        "name": "abhishek",
        "email": "022@ds.study.iitm.ac.in",
        "password": "abhishek",
        "roll_no": "022"
    }
```

   - Expected Output:  
     - `HTTP-Status Code: 400` 
     -`"message": "Email already registered"` 
   - Actual Output:  
     - `HTTP-Status Code: 400`
     -`"message": "Email already registered"`   
   - Result:  
     - `Passed`  
   - Pytest Code:

```
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
```


### Endpoint:

- **URL:** `http://127.0.0.1:5000/api/login`  
- **Method:** POST  
    
1. `def test_login_empty_inputs()` Tests whether the app correctly refutes empty inputs when the user tries to login  
     
   - Passed Inputs:  
     - `{"email": "", "password": ""}`  
   - Expected Output:  
     - `HTTP-Status Code: 400`  
   - Actual Output:  
     - `HTTP-Status Code: 400`  
   - Result:  
     - `Passed`  
   - Pytest Code:

```
def test_login_empty_inputs(client):
    data = {
        "email": "",
        "password": ""
    }
    response = client.post("/api/login", json=data)
    assert response.status_code == 400
    assert response.get_json()["message"] == "Email and password are required"
```

2. `def test_login_invalid_credentials()` Tests whether the app correctly rejects invalid username-password combination when the user tries to login  
     
   - Passed Inputs:  
     - `{"email": "newuser@email.com", "password": "wrongpassword"}`  
   - Expected Output:  
     - `HTTP-Status Code: 401`  
   - Actual Output:  
     - `HTTP-Status Code: 401`  
   - Result:  
     - `Passed`  
   - Pytest Code:

```
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
```

3. `def test_login_successful():` Tests whether the app lets the user log in if he gives correct credentials  
     
   - Passed Inputs:  
     - `{"email": "newuser@email.com", "password": "newpassword"}`  
   - Expected Output:  
     - `HTTP-Status Code: 200` 
     -`Json data with user details` 
   - Actual Output:  
     - `HTTP-Status Code: 200`
     -`Json data with user details`
   - Result:  
     - `Passed`  
   - Pytest Code:

```
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
```

# Course Work Recommendation API Tests

**Description:** These APIs provide recommendations for course materials and related content based on the user's query. The recommendations are tailored to the user's interests and past performance, aiming to enhance learning efficiency and engagement using Gen AI.

### Endpoint:

- **URL:** `http://127.0.0.1:5000/api/search`  
- **Method:** POST  
    
1. `def test_search_api()` Tests whether the app correctly gives the recommended study material based on the web search  
     
   - Passed Inputs:  
     - `{"query": "what is binary search"}`

   - Expected Output:  
     - `HTTP-Status Code: 200`  
   - Actual Output:  
     - `HTTP-Status Code: 200`  
   - Result:  
     - `Passed`  
   - Pytest Code:

```
def test_search_api(client: FlaskClient):
    """Test the search API (/api/search) with a query."""
    data = {"query": "what is binary search"}
    
    response = client.post("/api/search", json=data)
    json_data = response.get_json()

    # print("\nResponse JSON:", json_data)

    assert response.status_code == 200 # Ensure response contains expected key
    assert len(json_data)>=1# Ensure response contains expected key
```

2. `def test_search_empty_query()` Tests whether the app correctly rejects the incompatible inputs for the recommended search 
     
   - Passed Inputs:  
     - `{"query:""}`

   - Expected Output:  
     - `HTTP-Status Code: 400`
     -`"error": "Query parameter is required"`  
   - Actual Output:  
     - `HTTP-Status Code: 400`
     -`"error": "Query parameter is required"`  
   - Result:  
     - `Passed`  
   - Pytest Code:

```
def test_search_empty_query(client):
    data = {"query": ""}
    response = client.post("/api/search", json=data)
    assert response.status_code == 400
    assert response.json == {"error": "Query parameter is required"}
```

# Coding Assistance API Tests

**Description:** The Coding Assist API provides guidance and solutions for programming assignments by analyzing problem statements and error codes. It returns structured insights to help with debugging and understanding coding issues without giving direct code.

### Endpoint:

- **URL:** `http://127.0.0.1:5000/api/codeassist`  
- **Method:** POST  
    
1. `def test_code_assist_empty_inputs()` Tests whether the app correctly rejects invalid inputs, such as an empty problem_statement or error_code when generating solution.

   - ## Passed Inputs:

```
{"problem_statement": "","error_code":""}
```

   - Expected Output:  
     - `HTTP-Status Code: 400` or `404`  
   - Actual Output:  
     - `HTTP-Status Code: 404`  
   - Result:  
     - `Passed`  
   - Pytest Code:

```
def test_code_assist_empty_inputs(client):
    data = {"problem_statement": "", "error_code": ""}
    response = client.post("/api/codeassist", json=data)
    assert response.status_code == 400
    assert response.json == {"error": "Both problem statement and error code are required"}
```

2. `def test_codeassist_incomplete_params()` Tests whether the app correctly returns  error when the incomplete parameter is passed through it.

   - ## Passed Inputs:

```
{"problem_statement" : ""}
```

   - Expected Output:  
     - `HTTP-Status Code: 404`  
   - Actual Output:  
     - `HTTP-Status Code: 404`  
   - Result:  
     - `Passed`  
   - Pytest Code:

```
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
```

3. `def test_codeassist()`

   - ## Passed Inputs:

```
{
        "problem_statement": "find the odd number",
        "error_code": "if n%2==0; print('odd number')"
}
```

   - ## Expected Output:

```
HTTP-Status Code: 200
JSON solution
```

   - ## Actual Output:

```
HTTP-Status Code: 200
JSON Solution
```

   - ## Result:

     `Passed`  
       
   - Pytest Code:

```
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
```

# ChatAI API Testing

**description:** The ChatAI API handles general queries related to assignments and course-related support. It provides informative responses to help students with academic concepts.

### Endpoint:

- **URL:** `http://127.0.0.1:5000/api/chatai`  
- **Method:** POST  
    
1. `def test_chatai_empty_input()` Tests whether the app correctly rejects no inputs in message from the user during chat with chatbot using GenAI.  
     
   - Passed Inputs:  
     - `{ "query": ""} # message not there`  
   - Expected Output:  
     - `HTTP-Status Code: 400  # Bad Request`  
   - Actual Output:  
     - `HTTP-Status Code: 400`  
   - Result:  
     - `Passed`  
   - Pytest Code:

```
def test_chatai_empty_input(client):
    data = {
        "query": ""
    }
    response = client.post('/api/chatai', json=data)
    assert response.status_code == 400
    assert response.json == {
        "error": "Query parameter is required"
    }
```


2. `def test_chatai_api()` Tests whether the app correctly returns a response from the GenAI model when a valid message (not blank) from the student is passed in the chat.  
     
   - Passed Inputs:  
     - `{"query":"What is binary search?"}`  
   - Expected Output:  
     - `HTTP-Status Code: 200`
     - `JSON Response from Genai`  
   - Actual Output:  
     - `HTTP-Status Code: 200`
     - `JSON Response from Genai`  
   - Result:  
     - `Passed`  
   - Pytest Code:

```
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
```

# Support Chat API

**description:** This API uses RAG (Retrieval-Augmented Generation) to provide answers from the IITM BS portal, helping users navigate and resolve queries effectively.

### Endpoint:

- **URL:** `http://127.0.0.1:5000/api/support`  
- **Method:** POST  
1. `def test_support_api()` Tests whether the app correctly returns the answer asked by the user for general support for the IITM BS protal..  
   - Passed Inputs:  
     - `{
        "query": "how many credits are there in BS level?"
    }`    
   - Expected Output:  
     - `HTTP-Status Code: 200`
     - `JSON Answer`  
   - Actual Output:  
     - `HTTP-Status Code: 200` 
     - `JSON Answer` 
   - Result:  
     - `Passed`  
   - Pytest Code:

```
def test_support_api(client):
    # Define the query parameter
    data = {
        "query": "how many credits are there in BS level?"
    }

    # Send a POST request to /api/support
    response = client.post("/api/support", json=data)

    # Parse the response
    json_response = response.get_json()

    # Assertions
    assert response.status_code == 200
    assert json_response is not None
    assert len(json_response) > 0
```
2. `def test_support_empty_query()` Tests whether the app correctly rejects no inputs in message from the user during chat with chatbot using GenAI.  
     
   - Passed Inputs:  
     - `{ "query": ""} # message not there`  
   - Expected Output:  
     - `HTTP-Status Code: 400  # Bad Request`  
   - Actual Output:  
     - `HTTP-Status Code: 400`  
   - Result:  
     - `Passed`  
   - Pytest Code:

```
def test_support_empty_query(client):
    data = {"query": ""}
    response = client.post("/api/support", json=data)
    assert response.status_code == 400
    assert response.get_json() == {"error": "Query parameter is required"}
```


# Peer Group Recommendation API Testing

**Description:** This API recommends a peer study group based on students' marks using Gen AI. It ensures a balanced selection of high and low scorers for effective collaboration using GenAI model.

### Endpoint

- **URL:** `http://127.0.0.1:5000/api/study-group-recommendation`  
- **Method:** POST  
    
1. `def test_study_group_recommendation_invalid_input()` Tests getting  invalid inputs  
     
   - Passed Inputs:  
     - `{
        "roll_no": "050"  # Invalid roll number
    }`    
   - Expected Output:  
     - `HTTP-Status Code: 404` or `400`  
   - Actual Output:  
     - `HTTP-Status Code: 404`  
   - Result:  
     - `Passed`  
   - Pytest Code:

```
def test_study_group_recommendation_invalid_input(client):
    data = {
        "roll_no": "050"  # Invalid roll number
    }
    response = client.post('/api/study-group-recommendation', json=data)
    assert response.status_code == 500
    assert response.get_json() == {"error": "Object of type Response is not JSON serializable"}
```

2. `def test_study_group_recommendation_empty_input()` Tests getting  with empty inputs  
     
   - Passed Inputs:  
     -  `{"roll_no":""}`  
   - Expected Output:  
     - `HTTP-Status Code: 404` or `400`  
   - Actual Output:  
     - `HTTP-Status Code: 404`  
   - Result:  
     - `Passed`  
   - Pytest Code:

```
def test_study_group_recommendation_empty_input(client):
    data = {"roll_no":""}  # Empty input
    response = client.post('/api/study-group-recommendation', json=data)
    assert response.status_code == 400
    assert response.get_json() == {"error": "roll_no is required"}

```

3. `def test_study_group_recommendation_api()` Tests getting successfully  
     
   - Passed Inputs:  
     -  `{"roll_no":"002"}`  
   - Expected Output:  
     - `HTTP-Status Code: 200`  
   - Actual Output:  
     - `HTTP-Status Code: 200`  
   - Result:  
     - `Passed`  
   - Pytest Code:

```
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
```

# Generate Report API

**description:** Generates a detailed performance report in both HTML and PDF formats based on student marks data

- **URL:** `http://127.0.0.1:5000/api/generate-reports`  
- **Method:** GET  
    
1. `def test_generate_reports()` Tests whether the activity questions solved by the student can be submitted successfully.  
     
   - Passed Inputs: ``

   - ## Expected Output:

```
HTTP-Status Code: 200
JSON Parameter "results"
```

   - ## Actual Output:

```
HTTP-Status Code: 200
JSON Parameter "results"
```

   - Result:  
     - `Passed`  
   - Pytest Code:

```
def test_generate_reports(client):
    response = client.get('/api/generate-reports')  # Use GET method
    assert response.status_code == 200
    data = response.get_json()
    assert "response" in data
    assert "html_report_path" in data["response"]
    assert "pdf_report_path" in data["response"]
    assert data["response"]["html_report_path"] == "templates/report.html"
    assert data["response"]["pdf_report_path"] == "templates/report.pdf"
```
