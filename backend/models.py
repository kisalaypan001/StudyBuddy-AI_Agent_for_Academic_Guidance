from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.mutable import MutableList
from datetime import datetime
from flask_security import UserMixin, RoleMixin, AsaList, SQLAlchemyUserDatastore


db = SQLAlchemy()

class Student(db.Model):
    __tablename__ = 'students'
    
    roll_no = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    
    marks = relationship("Marks", back_populates="student", cascade="all, delete-orphan")

    def serialize(self):
        return {
            'roll_no': self.roll_no,
            'name': self.name,
            'email': self.email
        }

class Professor(db.Model):
    __tablename__ = 'professors'
    
    professor_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    
    marks = relationship("Marks", back_populates="professor")

    def serialize(self):
        return {
            'professor_id': self.professor_id,
            'name': self.name,
            'email': self.email,
            'subject': self.subject
        }

class Marks(db.Model):
    __tablename__ = 'marks'
    
    roll_no = Column(String, ForeignKey('students.roll_no'), primary_key=True)
    subject = Column(String, ForeignKey('professors.subject'), primary_key=True)
    quiz_1 = Column(db.Float, nullable=False)
    quiz_2 = Column(db.Float, nullable=False)
    end_term = Column(db.Float, nullable=False)
    
    student = relationship("Student", back_populates="marks")
    professor = relationship("Professor", back_populates="marks")

    def serialize(self):
        return {
            'roll_no': self.roll_no,
            'subject': self.subject,
            'quiz_1': self.quiz_1,
            'quiz_2': self.quiz_2,
            'end_term':self.end_term
        }
