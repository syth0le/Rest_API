import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields
from flask_migrate import Migrate

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), unique=True)
    summary = db.Column(db.String(128))
    steps = db.Column(db.String(128))

    def __init__(self, title, summary, steps):
        self.title = title
        self.summary = summary
        self.steps = steps

    def __str__(self):
        return self.title

    def __repr__(self):
        return '<Recipe %r>' % self.title


class RecipeSchema(ma.Schema):
    class Meta(ma.Schema.Meta):
        model = Recipe
        sqla_session = db.session

    id = fields.Number(dump_only=True)
    title = fields.String(required=True)
    summary = fields.String(required=True)
    steps = fields.String(required=True)


recipe_schema = RecipeSchema()
recipes_schema = RecipeSchema(many=True)


@app.route('/')
def index():
    return 'Hello World'


@app.route('/recipes', methods=['POST'])
def add_recipe():
    title = request.json['title']
    summary = request.json['summary']
    steps = request.json['steps']

    new_recipe = Recipe(title, summary, steps)

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
    recipe = Recipe.query.get(id)
    return recipe_schema.jsonify(recipe)


# Update a Recipe
@app.route('/recipes/<id>', methods=['PUT'])
def update_recipe(id):
    recipe = Recipe.query.get(id)

    recipe.title = request.json['title']
    recipe.summary = request.json['summary']
    recipe.steps = request.json['steps']

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