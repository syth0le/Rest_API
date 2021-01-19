from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
from rest_api.utils.db_init import db


class Steps(db.Model):
    __tablename__ = 'steps'

    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))
    name = db.Column(db.String(50), nullable=False)
    text = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<Steps %r>' % self.name

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


class StepsSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Steps
        sqla_session = db.session

    id = fields.Number(dump_only=True)
    name = fields.String(required=True)
    text = fields.String(required=True)
    recipe_id = fields.Integer()