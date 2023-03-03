from . import db
import datetime
from marshmallow import fields, Schema


class HazardModel(db.Model):
    __tablename__ = 'hazards'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    category = db.Column(db.String())
    geom = db.Column(db.String())
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)

    def __init__(self, data):
        """
        Class constructor
        """
        self.name = data.get('name')
        self.category = data.get('category')
        self.geom = data.get('geom')
        self.created_by = data.get('created_by')
        self.created_at = datetime.datetime.utcnow()
        self.modified_at = datetime.datetime.utcnow()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        self.modified_at = datetime.datetime.utcnow()
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all_hazards():
        return HazardModel.query.all()

    @staticmethod
    def get_one_hazard(id):
        return HazardModel.query.get(id)

    def __repr__(self):
        return f"<Hazard {self.name}>"


class HazardSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    category = fields.Str(required=True)
    geom = fields.Str(required=True)
    created_by = fields.Int(required=True)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
