import os
from flask import Flask
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from sqlalchemy import and_, or_

from rest_api.models.categories import Category, CategorySchema
from rest_api.models.ingredients import Ingredients , IngredientsSchema
from rest_api.utils.db_init import db
from flask import request, jsonify
from rest_api.models.recipes import RecipeSchema, Recipe


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)

with app.app_context():
    db.create_all()

ma = Marshmallow(app)
migrate = Migrate(app, db)


@app.route('/')
def index():
    return 'IT WORKS'


def json_getter(json_var):
    for unit in json_var:
        try:
            for element in json_var[unit]:
                print(f"{element}:", json_var[unit][element])
        except:
            print(f"{unit}:", json_var[unit])


@app.route('/recipes', methods=['POST'])
def add_recipe():
    data = request.get_json()
    recipe_schema = RecipeSchema()
    recipe = recipe_schema.load(data)
    result = recipe_schema.dump(recipe.create())
    return result
#    try:
#        data = request.get_json()
#        recipe_schema = RecipeSchema()
#        recipe = recipe_schema.load(data)
#        result = recipe_schema.dump(recipe.create())
#        return result
#    except Exception as e:
#        return "error 422"


# Get All Recipes
@app.route('/recipes', methods=['GET'])
def get_recipe_list():
    fetched = Recipe.get_all_recipes()
    recipe_schema = RecipeSchema(many=True)
    recipes = recipe_schema.dump(fetched)
    # pprint(recipes[0])
    return jsonify(recipes)


# Get Single Recipe by title
@app.route('/recipes/<string:title>', methods=['GET'])
def get_recipe_by_title(title):
    current_recipe = Recipe.find_recipe_by_title(title)
    # current_recipe = Recipe.query.get_or_404(id)
    recipe_schema = RecipeSchema()
    json_recipe = recipe_schema.dump(current_recipe)
    return jsonify(json_recipe)


# Get Single Recipe by id
@app.route('/recipes/<int:id>', methods=['GET'])
def get_recipe_by_id(id):
    # current_recipe = Recipe.query.get(id)
    current_recipe = Recipe.query.get_or_404(id)
    recipe_schema = RecipeSchema()
    json_recipe = recipe_schema.dump(current_recipe)
    return jsonify(json_recipe)


# Update a Recipe  написать еще по айдишнику)
@app.route('/recipes/<string:title>', methods=['PUT'])
def update_recipe(title):
    data = request.get_json()
    recipe_schema = RecipeSchema()
    recipe = recipe_schema.load(data)
    print(request.title)
    # print(type(recipe))
    # print(type(data))
    # print(data)
    current_recipe = Recipe.find_recipe_by_title(title)

    # for elem in recipe:
    #     print(elem)
    # result = recipe_schema.dump(current_recipe.update(data))
    # print(data.items())
    # current_recipe.update(data)

    return f"{title} updated"


# Delete Recipe
@app.route('/recipes/<string:title>', methods=['DELETE'])
def delete_recipe(title):
    current_recipe = Recipe.find_recipe_by_title(title)
    current_recipe.delete()
    return f"{title} deleted"


# Get Recipes by categories
@app.route('/recipes/category', methods=['GET'])
def get_recipes_by_category():
    try:
        extra = request.args.get('extra')
        if extra == 'all':
            categories = Category.query.with_entities(Category.name).distinct()
            categories_schema = CategorySchema(many=True)
            categories_json = categories_schema.dump(categories)
            return jsonify(categories_json)
    except:
        pass

    try:
        categories = request.args.get('categories').split(',')
    except:
        return jsonify({})

    categorized_recipes = Recipe.query.join(Category).filter(Category.name.in_(categories)).all()

    if len(categorized_recipes) == 0:
        return jsonify({})

    recipe_schema = RecipeSchema(many=True)
    json_recipe = recipe_schema.dump(categorized_recipes)
    return jsonify(json_recipe)


# Get Recipes by ingredient's filter
@app.route('/recipes/ingredients', methods=['GET'])
def get_recipes_by_filters():
    try:
        extra = request.args.get('extra')
        if extra == 'all':
            ingredients = Ingredients.query.with_entities(Ingredients.name).distinct()
            ingredients_schema = IngredientsSchema(many=True)
            ingredients_json = ingredients_schema.dump(ingredients)
            return jsonify(ingredients_json)
    except:
        pass

    try:
        ingredients = request.args.get('ingredients').split(',')
    except:
        return jsonify({})

    recipes_by_ingredients = Recipe.query.join(Ingredients).filter(Ingredients.name.in_(ingredients)).all()

    if len(recipes_by_ingredients) == 0:
        return jsonify({})

    recipe_schema = RecipeSchema(many=True)
    json_recipe = recipe_schema.dump(recipes_by_ingredients)
    return jsonify(json_recipe)
