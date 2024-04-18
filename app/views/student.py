from flask import Blueprint, request, jsonify
from app.models.student import Student
from app.database import db
from app.schemas.student_schema import StudentSchema
from flask_jwt_extended import jwt_required

student_blueprint = Blueprint("student", __name__)


@student_blueprint.route("/api/student", methods=["GET", "POST"])
def student_list():
    """Return all students from API"""

    if request.method == "GET":
        students = db.session.query(Student).all()
        if len(students) <= 0:
            error_msg = "No results."
            return jsonify(msg=error_msg, status=200), 200

        # TODO: Replace with schema dump and return JSON.
        print(students)
        result = []
        for student in students:
            result.append({
                'id': student.id,
                'name': student.name,
                'nationality': student.nationality,
                'city': student.city,
                'lat': student.lat,
                'long': student.long,
                'gender': student.gender,
                'age': student.age,
                'english_grade': student.english_grade,
                'maths_grade': student.maths_grade,
                'sciences_grade': student.sciences_grade,
                'languages_grade': student.languages_grade
            })
        return jsonify(result)

    else:

        # Get the JSON data from the request body.
        # Make sure to import 'request' from flask at the top.
        data = request.json

        # Try getting name, studentname, email and phone fields from our data, using dictionary indexing.
        try:
            name = data["name"]
            nationality = data["nationality"]
            city = data["city"]
            lat = data["lat"]
            long = data["long"]
            gender = data["gender"]
            age = data["age"]
            english_grade = data["english_grade"]
            maths_grade = data["maths_grade"]
            sciences_grade = data["sciences_grade"]
            languages_grade = data["languages_grade"]

            # Create a new instance of Student, passing in the required fields.
            new_student = Student(name=name, nationality=nationality, city=city, lat=lat, long=long,
                                  gender=gender, age=age, english_grade=english_grade, maths_grade=maths_grade,
                                  sciences_grade=sciences_grade, languages_grade=languages_grade)

            # Add the new student to the database.
            db.session.add(new_student)

            # Commit the transaction. This is required to actually save the new student.
            db.session.commit()

            success_msg = "New student created."

            # Return a success message, the same data that was sent in the request, and a 201 (Created) response status.
            return jsonify(msg=success_msg, data=data, status_code=201), 201

        # If there is a KeyError, this means that either 'name', 'studentname', 'email' and 'phone' are not present
        # in the request data.
        except KeyError:

            error_msg = "Please specify correct fields"
            return jsonify(msg=error_msg, status_code=400)


@student_blueprint.route("/api/student/<int:student_id>", methods=["GET"])
def get_single_student(student_id):
    """Return a single student from API."""

    student = db.session.query(Student).filter_by(id=student_id).first()
    if not student:
        error_msg = "Student not found. Try a different ID."
        return jsonify(msg=error_msg, status=200), 200

    print(student)

    result = [{
        'id': student.id,
        'name': student.name,
        'nationality': student.nationality,
        'city': student.city,
        'lat': student.lat,
        'long': student.long,
        'gender': student.gender,
        'age': student.age,
        'english_grade': student.english_grade,
        'maths_grade': student.maths_grade,
        'sciences_grade': student.sciences_grade,
        'languages_grade': student.languages_grade
    }]
    return jsonify(result)


@student_blueprint.route("/api/student/<int:student_id>", methods=["PATCH"])
def student_partial_update(student_id):
    """Perform partial update of student."""

    data = request.json

    student = db.session.query(Student).filter_by(id=student_id).first()
    if not student:
        error_msg = "Student does not exist. Try a different ID."
        return jsonify(msg=error_msg, status=400), 400

    try:
        for key, value in data.items():
            if not hasattr(student, key):
                raise ValueError
            else:
                setattr(student, key, value)
                db.session.commit()

        student = db.session.query(Student).filter_by(id=student_id).first()

        # TODO: Replace with schema dump and return as JSON.
        success_msg = f"Student with ID {student.id} updated."
        return success_msg, 200

    except ValueError:
        error_msg = "Error referencing columns with provided keys." \
                    " Student object contains <id>, <name>, <studentname>, <email> and <phone>."
        return jsonify(msg=error_msg, status=400), 400


@student_blueprint.route("/api/student/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    """Perform DELETE request to delete student."""

    student = db.session.query(Student).filter_by(id=student_id).first()
    msg = None
    if not student:
        msg = "Student not found."
    else:
        db.session.delete(student)
        db.session.commit()

        msg = f"Student with id {student_id} deleted."

    return msg, 200
    pass


