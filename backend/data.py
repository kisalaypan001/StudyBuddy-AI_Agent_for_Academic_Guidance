from flask_restful import Resource
from models import Student,Professor,db, Marks
from flask import jsonify , request

class StudentResource(Resource):
    def get(self):
        students = Student.query.all()
        return jsonify({
            'students': [student.serialize() for student in students]
        })

class ProfessorResource(Resource):
    def get(self):
        professors = Professor.query.all()
        return jsonify({
            'professors': [professor.serialize() for professor in professors]
        })
     
class MarksResource(Resource):
    def post(self):
        data = request.get_json()
        
        roll_no = data.get('roll_no')
        subject = data.get('subject')
        quiz_1 = data.get('quiz_1')
        quiz_2 = data.get('quiz_2')
        end_term= data.get('end_term')

        if not (roll_no and subject and  quiz_1 and quiz_2 is not None and end_term is not None):
            return {'message': 'Missing required fields'}, 400

        new_marks = Marks(roll_no=roll_no, subject=subject, quiz_1=quiz_1,quiz_2=quiz_2 ,end_term=end_term)
        db.session.add(new_marks)
        db.session.commit()

        return {'message': 'Marks added successfully'}, 201

    def get(self):
        marks = Marks.query.all()
        return jsonify([mark.serialize() for mark in marks])