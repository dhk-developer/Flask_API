from app.database import db
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import OperationalError, IntegrityError

import time


class AuthUser(db.Model):
    """Model to represent an Auth User in the DB."""

    __tablename__ = "auth_users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.password = generate_password_hash(password)

    def get_user(self, password):
        """Return auth user from database"""

        try:
            user = AuthUser.query.filter_by(email=self.email).first()
            if user:
                if check_password_hash(user.password, password):
                    return user
                else:
                    return "wrong password"
            else:
                return "not found"
        except Exception as e:
            print(f"Exception: {e}")
            return None

    def create_jwt_token(self):
        return create_access_token(self.email)

    @staticmethod
    def refresh_jwt_token(func):
        return create_access_token(identity=func())

    def add_user(self):

        num_retries = 5
        user_registration_success = False

        while num_retries > 0:
            try:
                db.session.add(self)
                db.session.commit()
                user_registration_success = True
                break
            except OperationalError:
                num_retries -= 1  # num_retries = num_retries - 1
                time.sleep(1)
            except IntegrityError:
                db.session.rollback()
                return False

        if not user_registration_success:
            return None
        else:
            return True







