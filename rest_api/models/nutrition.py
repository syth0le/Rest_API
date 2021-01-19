from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
from rest_api.utils.db_init import db


class Nutrition(db.Model):
    __tablename__ = 'nutrition'

    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))
    name = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    measure = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return '<Nutrition %r>' % self.name

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


class NutritionSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Nutrition
        sqla_session = db.session

    id = fields.Number(dump_only=True)
    name = fields.String(required=True)
    quantity = fields.Float(required=True)
    measure = fields.String(required=True)
    recipe_id = fields.Integer()