from . import db
import datetime
from . import bcrypt
from marshmallow import fields, Schema
from .HazardModel import HazardSchema


class UserModel(db.Model):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128), nullable=True)
    created_hazards = db.relationship('HazardModel', backref='users', lazy=True)

    def __init__(self, data):
        self.username = data.get('username')
        self.password = self.__generate_hash(data.get('password'))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            if key == 'password':
                self.password = self.__generate_hash(data.get('password'))
            setattr(self, key, item)
        self.modified_at = datetime.datetime.utcnow()
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __generate_hash(self, password):
        return bcrypt.generate_password_hash(password, rounds=10).decode('utf-8')

    def check_hash(self, password):
        return bcrypt.check_password_hash(self.password, password)

    @staticmethod
    def get_all_users():
        return UserModel.query.all()

    @staticmethod
    def get_one_user(id):
        return UserModel.query.get(id)

    @staticmethod
    def get_user_by_username(username):
        return UserModel.query.filter(UserModel.username==username).all()[0]

    def __repr__(self):
        return f"<User {self.username}>"


class UserSchema(Schema):
    user_id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    created_hazards = fields.Nested(HazardSchema, many=True)
