import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test_db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)


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

# /////////////////////////////////////////////////////////////////////////////////


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


recipe_schema = RecipeSchema()
recipes_schema = RecipeSchema(many=True)


@app.route('/')
def index():
    return 'Я РАБОТАЮ'


def json_getter(json_var):
    for unit in json_var:
        try:
            for element in json_var[unit]:
                print(f"{element}:", json_var[unit][element])
        except:
            print(f"{unit}:", json_var[unit])


@app.route('/recipes', methods=['POST'])
def add_recipe():
    title = request.json['title']
    steps = request.json['steps']  # тоже под них бд будет))

    summary = request.json['summary']
    json_getter(summary)
    nutrition = request.json['nutrition']
    json_getter(nutrition)
    ingredients = request.json['ingredients']
    json_getter(ingredients)
    images_paths = request.json['images_paths']
    json_getter(images_paths)

    category = request.json['category']
    slug = request.json['slug']
    date = request.json['date']

    print("title :", title)
    print("steps :", steps)
    print("category :", category)
    print("slug :", slug)
    print("date :", date)

    # new_recipe = Recipe(title, summary, ingredients, steps, nutrition)

    # db.session.add(new_recipe)
    # db.session.commit()
    return "okay"
    # return recipe_schema.jsonify(new_recipe)


# # Get All Recipes
# @app.route('/recipes', methods=['GET'])
# def get_recipes():
#     all_recipes = Recipe.query.all()
#     result = recipes_schema.dump(all_recipes)
#     return jsonify(result)
#
#
# # Get Single Recipe
# @app.route('/recipes/<id>', methods=['GET'])
# def get_recipe(id):
#     product = Recipe.query.get(id)
#     return recipe_schema.jsonify(product)
#
#
# # Update a Recipe
# @app.route('/recipes/<id>', methods=['PUT'])
# def update_recipe(id):
#     recipe = Recipe.query.get(id)
#
#     recipe.title = request.json['title']
#     recipe.summary = request.json['summary']
#     recipe.ingredients = request.json['ingredients']
#     recipe.steps = request.json['steps']
#     recipe.nutrition = request.json['nutrition']
#
#     db.session.commit()
#
#     return recipe_schema.jsonify(recipe)
#
#
# # Delete Recipe
# @app.route('/recipes/<id>', methods=['DELETE'])
# def delete_recipe(id):
#     recipe = Recipe.query.get(id)
#     db.session.delete(recipe)
#     db.session.commit()
#
#     return recipe_schema.jsonify(recipe)


if __name__ == "__main__":
    app.run()
