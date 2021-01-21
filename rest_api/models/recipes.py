from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
from rest_api.utils.db_init import db
from rest_api.models.categories import CategorySchema
from rest_api.models.summary import SummarySchema
from rest_api.models.nutrition import NutritionSchema
from rest_api.models.images import ImagesSchema
from rest_api.models.ingredients import IngredientsSchema
from rest_api.models.steps import StepsSchema


class Recipe(db.Model):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    title = db.Column(db.String(128), unique=True)
    slug = db.Column(db.String(128), unique=True)
    date = db.Column(db.String(128))
    steps = db.relationship("Steps", backref="recipe", cascade="all, delete-orphan")
    category = db.relationship("Category", backref="recipe", cascade="all, delete-orphan")
    summary = db.relationship("Summary", backref="recipe", cascade="all, delete-orphan")
    nutrition = db.relationship("Nutrition", backref="recipe", cascade="all, delete-orphan")
    images = db.relationship("Images", backref="recipe", cascade="all, delete-orphan")
    ingredients = db.relationship("Ingredients", backref="recipe", cascade="all, delete-orphan")

    def __str__(self):
        return self.title

    def __repr__(self):
        return '<Recipe %r>' % self.title

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, data):
        for key, item in data:
            setattr(self, key, item)
        # self.modified_at = datetime.datetime.utcnow()
        db.session.commit()

    @classmethod
    def get_all_recipes(cls):
        return cls.query.all()

    @classmethod
    def find_recipe_by_title(cls, title):
        return cls.query.filter_by(title=title).first()


    # @classmethod
    # def convertation_json(cls, title):
    #     recipe_obj = cls.query.filter_by(title=title).first()


class RecipeSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Recipe
        sqla_session = db.session

    id = fields.Number(dump_only=True)
    title = fields.String(required=True)
    slug = fields.String(required=True)
    date = fields.String(required=True)
    category = fields.Nested(CategorySchema, many=True, only=['name', 'id'])
    summary = fields.Nested(SummarySchema, many=True, only=['name', 'quantity', 'measure', 'id'])
    nutrition = fields.Nested(NutritionSchema, many=True, only=['name', 'quantity', 'measure', 'id'])
    images = fields.Nested(ImagesSchema, many=True, only=['name', 'slug', 'id'])
    ingredients = fields.Nested(IngredientsSchema, many=True, only=['name', 'quantity', 'id'])
    steps = fields.Nested(StepsSchema, many=True, only=['name', 'text', 'id'])
