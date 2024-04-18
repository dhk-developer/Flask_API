from app.database import db

class Address(db.Model):
    """Model to produce address table for database."""

    __tablename__ = "address"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    house_name = db.Column(db.String(200), nullable=False)
    road = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(200), nullable=False)
    state = db.Column(db.String(200), nullable=False)
    country = db.Column(db.String(200), nullable=False)
    zipcode = db.Column(db.String(30), nullable=False)
    student = db.relationship("Student", back_populates="address")

    def __init__(self, student_id, number, house_name, road, city, state, country, zipcode):
        self.student_id = student_id
        self.number = number
        self.house_name = house_name
        self.road = road
        self.city = city
        self.state = state
        self.country = country
        self.zipcode = zipcode


    def __str__(self):
        return (f"Address of student {self.student_id}: {self.number}, {self.house_name} \n {self.road} \n {self.city}, {self.state} \n"
                f"{self.country} \n {self.zipcode}")
