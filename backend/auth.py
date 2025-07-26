from flask import Blueprint, request, jsonify
from flask_restful import Resource, Api, reqparse, fields, marshal
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Student, Professor



class register(Resource):
    def post(self):
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        roll_no = data.get('roll_no')

        if not name or not email or not password or not roll_no:
            return {'message': 'All fields are required'}, 400

        if Student.query.filter_by(email=email).first():
            return {'message': 'Email already registered'}, 400

        hashed_password = generate_password_hash(password)

        new_student = Student(name=name, email=email, password=hashed_password, roll_no=roll_no)
        db.session.add(new_student)
        db.session.commit()

        return {'message': 'Student registered successfully'}, 201

# Login API
class login(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return {'message': 'Email and password are required'}, 400

        student = Student.query.filter_by(email=email).first()

        if not student or not check_password_hash(student.password, password):
            return {'message': 'Invalid credentials'}, 401

        return {
            'message': 'Login successful',
            'student': {
                'name': student.name,
                'email': student.email,
                'roll_no': student.roll_no
            }
        }, 200
    

    ### Professor Registration ###
class ProfRegister(Resource):
    def post(self):
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        subject = data.get('subject')

        if Professor.query.filter_by(email=email).first():
            return {'message': 'Email already exists'}, 400

        hashed_password = generate_password_hash(password)

        new_professor = Professor(name=name, email=email, password=hashed_password,subject=subject)
        db.session.add(new_professor)
        db.session.commit()

        return {'message': 'Professor registered successfully'}, 201


### Professor Login ###
class ProfLogin(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        professor = Professor.query.filter_by(email=email).first()

        if professor and check_password_hash(professor.password, password):
            return jsonify(professor.serialize())

        return {'message': 'Invalid email or password'}, 401