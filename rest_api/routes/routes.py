# from flask import request, jsonify
# from rest_api.models.recipes import RecipeSchema, Recipe
# from main import app
#
#
# @app.route('/')
# def index():
#     return 'IT WORKS'
#
#
# def json_getter(json_var):
#     for unit in json_var:
#         try:
#             for element in json_var[unit]:
#                 print(f"{element}:", json_var[unit][element])
#         except:
#             print(f"{unit}:", json_var[unit])
#
#
# @app.route('/recipes', methods=['POST'])
# def add_recipe():
#     try:
#         data = request.get_json()
#         recipe_schema = RecipeSchema()
#         recipe = recipe_schema.load(data)
#         result = recipe_schema.dump(recipe.create())
#         print(result)
#         return "okay"
#     except Exception as e:
#         return "error 422"
#
#
# # Get All Recipes
# @app.route('/recipes', methods=['GET'])
# def get_recipe_list():
#     fetched = Recipe.get_all_recipes()
#     recipe_schema = RecipeSchema(many=True)
#     recipes = recipe_schema.dump(fetched)
#     # pprint(recipes[0])
#     return jsonify(recipes)
#
#
# # Get Single Recipe
# @app.route('/recipes/<string:title>', methods=['GET'])
# def get_recipe(title):
#     current_recipe = Recipe.find_recipe_by_title(title)
#     # current_recipe = Recipe.query.get_or_404(id)
#     recipe_schema = RecipeSchema()
#     json_recipe = recipe_schema.dump(current_recipe)
#     return jsonify(json_recipe)
#
#
# # Update a Recipe
# @app.route('/recipes/<string:title>', methods=['PUT'])
# def update_recipe(title):
#     data = request.get_json()
#     recipe_schema = RecipeSchema()
#     recipe = recipe_schema.load(data)
#     print(request.title)
#     # print(type(recipe))
#     # print(type(data))
#     # print(data)
#     current_recipe = Recipe.find_recipe_by_title(title)
#
#     # for elem in recipe:
#     #     print(elem)
#     # result = recipe_schema.dump(current_recipe.update(data))
#     # print(data.items())
#     # current_recipe.update(data)
#
#     return f"{title} updated"
#
#
# # Delete Recipe
# @app.route('/recipes/<string:title>', methods=['DELETE'])
# def delete_recipe(title):
#     current_recipe = Recipe.find_recipe_by_title(title)
#     current_recipe.delete()
#     return f"{title} deleted"
