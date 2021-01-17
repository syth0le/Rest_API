import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

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
    steps = db.relationship("Steps", backref="recipe")
    category = db.relationship("Category", backref="recipe")
    summary = db.relationship("Summary", backref="recipe")
    nutrition = db.relationship("Nutrition", backref="recipe")
    images = db.relationship("Images", backref="recipe")
    ingredient = db.relationship("Ingredients", backref="recipe")

    def __init__(self, title, steps):
        self.title = title
        self.steps = steps

    def __str__(self):
        return self.title

    def __repr__(self):
        return '<Recipe %r>' % self.title
    """метод для вывода всего или что то там(крч метод all)чтобы сразу все собрать в json И не ебать себе мозг"""

    def convertation_json(self, title):
        recipe_obj = Recipe.query.filter_by(title=title)




class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Category %r>' % self.name


class Summary(db.Model):
    __tablename__ = 'summary'

    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))
    name = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    measure = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return '<Summary %r>' % self.name


class Nutrition(db.Model):
    __tablename__ = 'nutrition'

    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))
    name = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    label = db.Column(db.String(50), nullable=False)
    measure = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return '<Nutrition %r>' % self.name


class Images(db.Model):
    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))
    name = db.Column(db.String(50), unique=True, nullable=False)
    slug = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return '<Images %r>' % self.name


class Ingredients(db.Model):
    __tablename__ = 'ingredients'

    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))
    name = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return '<Ingredients %r>' % self.name


class Steps(db.Model):
    __tablename__ = 'steps'

    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))
    title = db.Column(db.String(50), nullable=False)
    text = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<Steps %r>' % self.name

class RecipeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Recipe
        include_relationships = True
        load_instance = True


class SummarySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Summary
        include_fk = True
        load_instance = True


class ImageSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Images
        include_fk = True
        load_instance = True


class IngredientSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Ingredients
        include_fk = True
        load_instance = True


class CategorySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Category
        include_fk = True
        load_instance = True


class NutritionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Nutrition
        include_fk = True
        load_instance = True


# class NutritionSchema(ma.Schema):
#     class Meta(ma.Schema.Meta):
#         model = Nutrition
#         sqla_session = db.session
#
#     id = fields.Number(dump_only=True)
#     name = fields.String(required=True)
#     recipe_id = fields.Integer()
#
#
# class RecipeSchema(ma.Schema):
#     class Meta(ma.Schema.Meta):
#         model = Recipe
#         sqla_session = db.session
#
#     id = fields.Number(dump_only=True)
#     title = fields.String(required=True)
#     summary = fields.String(required=True)
#     steps = fields.String(required=True)
#     nutrition = fields.Nested(NutritionSchema, many=True, only=['id', 'name'])


# from models import *
# >>> recipe = Recipe(title="recipe 1", steps="steps_1")
# >>> db.session.add(recipe)
# >>> db.session.commit()
#
#  nutrition_1 = Nutrition(name="iron", quantity=23, label="iron", measure="mg", recipe=recipe)
# >>> db.session.add(nutrition_1)
# >>> nutrition_2 = Nutrition(name="Ca", quantity=35, label="calcium", measure="mg", recipe=recipe)
# >>> db.session.add(nutrition_2)
# >>> db.session.commit()
# recipe_get = Recipe.query.filter_by(title="recipe 1")
# >>> recipe_get
# <flask_sqlalchemy.BaseQuery object at 0x000001B74275DC08>
# >>> recipe.nutrition
# [<Nutrition 'iron'>, <Nutrition 'Ca'>]
# >>>

