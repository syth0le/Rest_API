import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
from pprint import pprint

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


# recipe_schema = RecipeSchema()
# recipes_schema = RecipeSchema(many=True)


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
    try:
        data = request.get_json()
        recipe_schema = RecipeSchema()
        recipe = recipe_schema.load(data)
        result = recipe_schema.dump(recipe.create())
        print(result)
        return "okay"
    except Exception as e:
        return "error 422"


# Get All Recipes
@app.route('/recipes', methods=['GET'])
def get_recipe_list():
    fetched = Recipe.get_all_recipes()
    recipe_schema = RecipeSchema(many=True)
    recipes = recipe_schema.dump(fetched)
    # pprint(recipes[0])
    return jsonify(recipes)


# Get Single Recipe
@app.route('/recipes/<string:title>', methods=['GET'])
def get_recipe(title):
    current_recipe = Recipe.find_recipe_by_title(title)
    # current_recipe = Recipe.query.get_or_404(id)
    recipe_schema = RecipeSchema()
    json_recipe = recipe_schema.dump(current_recipe)
    return jsonify(json_recipe)


# Update a Recipe
@app.route('/recipes/<string:title>', methods=['PUT'])
def update_recipe(title):
    data = request.get_json()
    recipe_schema = RecipeSchema()
    recipe = recipe_schema.load(data)
    # print(type(recipe))
    # print(type(data))
    # print(data)
    current_recipe = Recipe.find_recipe_by_title(title)

    for elem in recipe:
        print(elem)
    # result = recipe_schema.dump(current_recipe.update(data))
    # print(data.items())
    # current_recipe.update(data)

    return f"{title} updated"


# Delete Recipe
@app.route('/recipes/<string:title>', methods=['DELETE'])
def delete_recipe(title):
    current_recipe = Recipe.find_recipe_by_title(title)
    db.session.delete(current_recipe)
    db.session.commit()
    return f"{title} deleted"


if __name__ == "__main__":
    app.run()
