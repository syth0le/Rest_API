import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from models import *

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test_db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)

# recipe_schema = RecipeSchema()
# recipes_schema = RecipeSchema(many=True)


@app.route('/')
def index():
    return 'Я РАБОТАЮ'


@app.route('/recipes', methods=['POST'])
def add_recipe():
    title = request.json['title']
    summary = request.json['summary']
    ingredients = request.json['ingredients']
    steps = request.json['steps']
    nutrition = request.json['nutrition']

    new_recipe = Recipe(title, summary, ingredients, steps, nutrition)

    db.session.add(new_recipe)
    db.session.commit()

    return recipe_schema.jsonify(new_recipe)


# Get All Recipes
@app.route('/recipes', methods=['GET'])
def get_recipes():
    all_recipes = Recipe.query.all()
    result = recipes_schema.dump(all_recipes)
    return jsonify(result)


# Get Single Recipe
@app.route('/recipes/<id>', methods=['GET'])
def get_recipe(id):
    product = Recipe.query.get(id)
    return recipe_schema.jsonify(product)


# Update a Recipe
@app.route('/recipes/<id>', methods=['PUT'])
def update_recipe(id):
    recipe = Recipe.query.get(id)

    recipe.title = request.json['title']
    recipe.summary = request.json['summary']
    recipe.ingredients = request.json['ingredients']
    recipe.steps = request.json['steps']
    recipe.nutrition = request.json['nutrition']

    db.session.commit()

    return recipe_schema.jsonify(recipe)


# Delete Recipe
@app.route('/recipes/<id>', methods=['DELETE'])
def delete_recipe(id):
    recipe = Recipe.query.get(id)
    db.session.delete(recipe)
    db.session.commit()

    return recipe_schema.jsonify(recipe)


if __name__ == "__main__":
    app.run()
