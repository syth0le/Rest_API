from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
from rest_api.utils.db_init import db


class Ingredients(db.Model):
    __tablename__ = 'ingredients'

    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))
    name = db.Column(db.String(50), unique=True, nullable=False)
    quantity = db.Column(db.Integer, unique=True, nullable=True)

    def __repr__(self):
        return '<Ingredients %r>' % self.name

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


class IngredientsSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Ingredients
        sqla_session = db.session

    id = fields.Number(dump_only=True)
    name = fields.String(required=True)
    quantity = fields.Integer(required=True)
    recipe_id = fields.Integer()