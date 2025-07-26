import os
from dotenv import load_dotenv
from groq import Groq
import re
import json
from flask import jsonify,request
from models import *

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def study_group_recommended_f(roll_number):
    student_marks = Marks.query.filter_by(roll_no=roll_number).all()
    if not student_marks:
        return jsonify({'error': 'Student not found'}), 404

    students = Marks.query.filter(Marks.quiz_1.isnot(None)).all()

    all_students_data = [{'roll_no':s.roll_no,'subject':s.subject,'quiz_1':s.quiz_1} for s in students]
    student_data = [{'roll_no':s.roll_no,'subject':s.subject,'quiz_1':s.quiz_1} for s in student_marks]
    client = Groq(
        api_key=GROQ_API_KEY,
    )
    
    prompt = f"""
    Given the students list {all_students_data}, recommend exactly 5 unique students to {student_data}. 
    Ensure a balanced selection, including both high and low scorers.

    Return a JSON-formatted list containing only the recommended students. 
    Each student should be represented as a dictionary with:
    - "roll_no": roll number
    - "subject": subject
    - "quiz1": quiz1 score
    """


    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        # model="llama-3.3-70b-versatile",
        # model="llama-3.2-90b-vision-preview",
        model="deepseek-r1-distill-llama-70b",
        # model="gemma2-9b-it",
        # model="mixtral-8x7b-32768",
    )
    # print(chat_completion.choices[0].message.content)
    # Regular expression pattern to extract the JSON array
    pattern = r"\[\s*\{.*?\}\s*\]"

    # Using regex to find JSON-like structure
    match = re.search(pattern, chat_completion.choices[0].message.content, re.DOTALL)

    if match:
        extracted_json = match.group()  
        students_list = json.loads(extracted_json) 
    else:
        print("No valid JSON found")

    recommended_students = []
    for student in students_list:
        student_record = Student.query.filter_by(roll_no=student["roll_no"]).first()
        if student_record:
            recommended_students.append({
                "name": student_record.name,
                "email": student_record.email
            })
    return recommended_students