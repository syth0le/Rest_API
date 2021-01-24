from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
from rest_api.utils.db_init import db


class Images(db.Model):
    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))
    slug = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Images %r>' % self.slug

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


class ImagesSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Images
        sqla_session = db.session

    id = fields.Number(dump_only=True)
    slug = fields.String(required=True)
    recipe_id = fields.Integer()