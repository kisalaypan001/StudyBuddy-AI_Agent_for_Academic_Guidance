from flask import Flask, request, jsonify,send_from_directory
from flask_cors import CORS
from search import SearchResults
from coding_assist import programming_assist
from support import SupportChat
from flask_sqlalchemy import SQLAlchemy
from models import db
from chat import chatAI
from flask_restful import Api
from auth import login, register, ProfRegister, ProfLogin
from report import analysis_and_report_f
from group_recommendation import study_group_recommended_f
import csv
import io
from nav import query_rag
from prompt_search import is_query_education_related, get_ai_response, search_results
from flask import send_file
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import groq
from langchain_community.tools import DuckDuckGoSearchResults
import re



app = Flask(__name__, static_folder="frontend/my-vue-spa/public", static_url_path="/")
limiter = Limiter(key_func=get_remote_address)
limiter.init_app(app)
API_KEY = "your Key"

CORS(app) 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)

db.init_app(app)

from models import *

# Create all tables
with app.app_context():
    db.create_all() # Enable Cross-Origin Resource Sharing


api.add_resource(login, '/api/login')
api.add_resource(register, '/api/register')
api.add_resource(ProfRegister, '/api/professor/register')
api.add_resource(ProfLogin, '/api/professor/login')

from data import StudentResource, ProfessorResource,MarksResource
api.add_resource(StudentResource,'/api/students')
api.add_resource(ProfessorResource,'/api/professors')
api.add_resource(MarksResource,'/api/addMarks')
from flask import redirect



@app.route("/", methods=["GET"])
def home():
    return redirect("http://localhost:8080/")

@app.route("/api/ask", methods=["POST"])
def ask():
    """API endpoint to query RAG system."""
    data = request.json
    question = data.get("question")
    
    if not question:
        return jsonify({"error": "Question is required"}), 400
    
    answer = query_rag(question)
    return jsonify({"answer": answer})

@app.route("/api/prompt_search", methods=["POST"])
@limiter.limit("5 per minute")  # Apply rate limit
def search():
    data = request.json
    query = data.get("query") if data else None

    if not query:
        return jsonify({"error": "Query is required."}), 400

    # Step 1: Ask AI if the query is truly education-related
    if is_query_education_related(API_KEY, query):
        # Step 2: If AI confirms, fetch AI-generated response
        ai_response = get_ai_response(API_KEY, query)
        md_results = search_results(query)
    else:
        return jsonify({"error": "This query is not related to education. Please ask an academic question."}), 400

    return jsonify({"query": query, "ai_response": ai_response, "md_results": md_results}), 200

@app.route('/api/search', methods=['POST'])
def search_api():
    try:
        # Get JSON data from request
        data = request.get_json()
        user_query = data.get("query", "")

        if not user_query:
            return jsonify({"error": "Query parameter is required"}), 400

        # Invoke the SearchResults function
        result = SearchResults(user_query)
        
        return jsonify({"response": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/codeassist', methods=['POST'])
def code_assist():
    data = request.get_json()
    problem_statement = data.get('problem_statement', '')
    error_code = data.get('error_code', '')
    
    if not problem_statement or not error_code:
        return jsonify({'error': 'Both problem statement and error code are required'}), 400
    
    response = programming_assist(problem_statement, error_code)
    return jsonify({'response': response})

@app.route('/api/support', methods=['POST'])
def support_chat():
    try:
        data = request.get_json()
        query = data.get("query", "")
        
        if not query:
            return jsonify({"error": "Query parameter is required"}), 400
        
        bot = SupportChat()
        result=bot.chat(query)
        return jsonify({"response": result})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/chatai', methods=['POST'])
def chat_api():
    try:
        data = request.get_json()  # Get JSON data from request
        query = data.get('query')  # Extract query parameter

        if not query:
            return jsonify({"error": "Query parameter is required"}), 400

        response = chatAI(query)  # Call the chat function
        return jsonify({"response": response})  # Return response as JSON

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/study-group-recommendation', methods=['POST'])
def group_recommend_f():
    try:
        data = request.get_json() 
        roll_number = data.get('roll_no','')
        if not roll_number:
            return jsonify({'error': 'roll_no is required'}), 400
        response = study_group_recommended_f(roll_number)
        return jsonify({"response": response})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

################ Analysis and Report Generation API ###############
@app.route('/api/generate-reports', methods=['POST'])
def report_f():
    try:
        data = request.get_json()
        subject = data.get('subject', '')
        
        # Updated logic that calls your enhanced report function
        report_data = analysis_and_report_f(subject)
        
        return jsonify(report_data)

    except Exception as e:
        print("❌ Report Generation Error:", e)
        return jsonify({"response": {
            "summary": "Summary generation failed.",
            "pdf_ready": False
        }}), 500


@app.route('/api/get-report-pdf', methods=['GET'])
def get_report_pdf():
    try:
        return send_file("templates/Report.pdf", as_attachment=False)
    except Exception as e:
        print("❌ PDF Fetch Error:", e)
        return jsonify({"error": str(e)}), 500

@app.route('/templates/<path:filename>')
def serve_template_files(filename):
    return send_from_directory('templates', filename)


@app.route('/api/students/all', methods=['GET'])
def get_all_students():
    students = Student.query.all()
    result = []
    for s in students:
        marks = []
        for m in s.marks:
            marks.append({
                'subject': m.subject,
                'quiz_1': m.quiz_1,
                'quiz_2': m.quiz_2,
                'end_term': m.end_term
            })
        result.append({
            'id': s.roll_no,
            'rollNo': s.roll_no,
            'name': s.name,
            'email': s.email,
            'marks': marks
        })
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)