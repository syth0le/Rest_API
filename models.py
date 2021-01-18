import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test_db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


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

    @classmethod
    def find_recipe_by_title(cls, title):
        return cls.query.filter_by(title=title).first()

    """метод для вывода всего или что то там(крч метод all)чтобы сразу все собрать в json И не ебать себе мозг"""
    #  но нужен ли он блять
    # @classmethod
    # def convertation_json(cls, title):
    #     recipe_obj = cls.query.filter_by(title=title).first()


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Category %r>' % self.name

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


class Summary(db.Model):
    __tablename__ = 'summary'

    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))
    name = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    measure = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return '<Summary %r>' % self.name

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


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


class Images(db.Model):
    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))
    name = db.Column(db.String(50), unique=True, nullable=False)
    slug = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return '<Images %r>' % self.name

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


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


class CategorySchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Category
        sqla_session = db.session

    id = fields.Number(dump_only=True)
    name = fields.String(required=True)
    recipe_id = fields.Integer()


class SummarySchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Summary
        sqla_session = db.session

    id = fields.Number(dump_only=True)
    name = fields.String(required=True)
    quantity = fields.Integer(required=True)
    measure = fields.String(required=True)
    recipe_id = fields.Integer()


class NutritionSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Nutrition
        sqla_session = db.session

    id = fields.Number(dump_only=True)
    name = fields.String(required=True)
    quantity = fields.Float(required=True)
    measure = fields.String(required=True)
    recipe_id = fields.Integer()


class ImagesSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Images
        sqla_session = db.session

    id = fields.Number(dump_only=True)
    name = fields.String(required=True)
    slug = fields.String(required=True)
    recipe_id = fields.Integer()


class IngredientsSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Ingredients
        sqla_session = db.session

    id = fields.Number(dump_only=True)
    name = fields.String(required=True)
    quantity = fields.Integer(required=True)
    recipe_id = fields.Integer()


class StepsSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Steps
        sqla_session = db.session

    id = fields.Number(dump_only=True)
    name = fields.String(required=True)
    text = fields.String(required=True)
    recipe_id = fields.Integer()


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

