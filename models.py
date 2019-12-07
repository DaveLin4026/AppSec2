import datetime
import enum

from flask_login import UserMixin
from werkzeug.security import generate_password_hash

from app import db


class Roles(enum.Enum):
    admin = "admin"
    user = "user"


class User(UserMixin, db.Model):
#  inherit from UserMixin, which provides default implementations for all of these properties and methods.
    __tablename__ = "cuser"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_authenticated = db.Column(db.Boolean)
    is_active = db.Column(db.Boolean)
    role = db.Column(db.Enum(Roles))
    two_factor = db.Column(db.String(80))

    is_anonymous = False

    def __init__(self, username, password, role=Roles.user, two_factor=""):
        self.username = username
        self.password = password
        self.role = role
        self.two_factor = two_factor

    def hash_and_save(self):
        self.password = generate_password_hash(self.password)
        return self.save()

    def save(self):
        existing_user = self.__class__.query.filter_by(username=self.username).first()
        if existing_user is None:
            db.session.add(self)
        db.session.commit()
        return self

    def create_session(self):
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False

    @property
    def is_admin(self):
        return True if self.role == Roles.admin else False


class SpellCheck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text_to_check = db.Column(db.Text())
    result = db.Column(db.Text())
    user_id = db.Column(db.Integer, db.ForeignKey("cuser.id"))
    user = db.relationship("User")

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def can_be_accessed_by(self, user):
        if self.user.id == user.id or user.role == Roles.admin:
            return True
        return False


class UserActivity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    activity_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    activity_name = db.Column(db.String(80))

    user_id = db.Column(db.Integer, db.ForeignKey("cuser.id"))
    user = db.relationship("User")

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

# Database Users Function
def create_database_users():
    test_user = User(
        username="test", password="test", two_factor="12345678901", role=Roles.admin
    )
    test_user.hash_and_save()

    admin_user = User(
        username="admin",
        password="Administrator@1",
        two_factor="12345678901",
        role=Roles.admin,
    )
    admin_user.hash_and_save()

    unauth_user = User(username="unauth", password="test", two_factor="12345678901",)
    unauth_user.hash_and_save()
