"""
Remember to import your SQLAlchemy instance!
"""

from app.database import db


class Student(db.Model):
    """Model to represent a student record in database."""

    __tablename__ = "student"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    nationality = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(200), nullable=False)
    lat = db.Column(db.String(50), nullable=False)
    long = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(3), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    english_grade = db.Column(db.Integer, nullable=False)
    maths_grade = db.Column(db.Integer, nullable=False)
    sciences_grade = db.Column(db.Integer, nullable=False)
    languages_grade = db.Column(db.Integer, nullable=False)
    address = db.relationship("Address", uselist=False, cascade="all, delete-orphan")

    def __init__(self, name, nationality, city, lat, long, gender, age, english_grade, maths_grade, sciences_grade, languages_grade):
        self.name = name
        self.nationality = nationality
        self.city = city
        self.lat = lat
        self.long = long
        self.gender = gender
        self.age = age
        self.english_grade = english_grade
        self.maths_grade = maths_grade
        self.sciences_grade = sciences_grade
        self.languages_grade = languages_grade

    def __repr__(self):
        return (f"Student(id={self.id}, name={self.name}, nationality={self.nationality}, city={self.city},"
                f" lat={self.lat}, long={self.long}, gender={self.gender}, age={self.age},"
                f" english_grade={self.english_grade}, maths_grade={self.maths_grade}, sciences_grade={self.sciences_grade},"
                f" languages_grade={self.languages_grade}")
