from app.serializer import ma
from app.models.student import Student
from app.schemas.address_schema import AddressSchema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class StudentSchema(SQLAlchemyAutoSchema):
    """Serializable schema for the Student SQLAlchemy object."""

    class Meta:
        # Provide the User model to serialize.
        model = Student

        # Define the fields which will be in the output when User model is serialized.
        fields = ("id", "name", "nationality", "city", "lat", "long", "gender", "age", "english_grade", "maths_grade",
                  "sciences_grade", "languages_grade")

    addresses = ma.Nested(AddressSchema, many=True)
