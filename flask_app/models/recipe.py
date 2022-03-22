from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import member

class Recipe:
    db_name = 'family_cookbook_schema'
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.ingredients = data['ingredients']
        self.instructions = data['instructions']
        self.under_30 = data['under_30']
        self.category = data['category']
        self.member_id = data['member_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None

    @classmethod
    def create(cls, data):
        query = "INSERT INTO recipes (name, ingredients, instructions, under_30, category, member_id) VALUES (%(name)s, %(ingredients)s, %(instructions)s, %(under_30)s, %(category)s, %(member_id)s);"
        return connectToMySQL(cls.db_name).query_db(query,data)


    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes;"
        result = connectToMySQL(cls.db_name).query_db(query)
        all_recipes = []
        for row in result:
            all_recipes.append( cls(row) )
        return all_recipes

    @classmethod
    def get_all_recipes_with_member(cls):
        query = "SELECT * FROM recipes JOIN members ON recipes.member_id = members.id;"
        results = connectToMySQL(cls.db_name).query_db(query)
        recipes = []
        for row in results:
            one_recipe = cls(row)
            one_recipes_member_info = {
                "id": row['members.id'], 
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": row['password'],
                "created_at": row['members.created_at'],
                "updated_at": row['members.updated_at']
                }
            adder = member.Member(one_recipes_member_info)
            one_recipe.creator = adder
            recipes.append(one_recipe)
        return recipes


    @classmethod
    def get_all_recipes_from_one_member(cls, data):
        query = "SELECT * FROM recipes JOIN members ON recipes.member_id = members.id WHERE member_id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        recipes = []
        for row in results:
            one_recipe = cls(row)
            one_recipes_member_info = {
                "id": row['members.id'], 
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": row['password'],
                "created_at": row['members.created_at'],
                "updated_at": row['members.updated_at']
                }
            adder = member.Member(one_recipes_member_info)
            one_recipe.creator = adder
            recipes.append(one_recipe)
        return recipes

    @classmethod
    def get_one_recipe_with_member(cls, data):
        query = "SELECT * FROM recipes JOIN members ON recipes.member_id = members.id WHERE recipes.id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        one_recipe = cls(results[0])
        one_recipes_member_info = {
            "id": results[0]['members.id'], 
            "first_name": results[0]['first_name'],
            "last_name": results[0]['last_name'],
            "email": results[0]['email'],
            "password": results[0]['password'],
            "created_at": results[0]['members.created_at'],
            "updated_at": results[0]['members.updated_at']
            }
        adder = member.Member(one_recipes_member_info)
        one_recipe.creator = adder
        return one_recipe

    @classmethod
    def get_recipe_by_id(cls,data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        result = connectToMySQL(cls.db_name).query_db(query,data)
        return cls(result[0])

    @classmethod
    def get_all_recipes_from_category(cls, data):
        query = "SELECT * FROM recipes JOIN members ON recipes.member_id = members.id WHERE category = %(category)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        recipes = []
        for row in results:
            one_recipe = cls(row)
            one_recipes_member_info = {
                "id": row['members.id'], 
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": row['password'],
                "created_at": row['members.created_at'],
                "updated_at": row['members.updated_at']
                }
            adder = member.Member(one_recipes_member_info)
            one_recipe.creator = adder
            recipes.append(one_recipe)
        return recipes

    @classmethod
    def get_all_recipes_from_under_30(cls, data):
        query = "SELECT * FROM recipes JOIN members ON recipes.member_id = members.id WHERE under_30 = %(under_30)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        recipes = []
        for row in results:
            one_recipe = cls(row)
            one_recipes_member_info = {
                "id": row['members.id'], 
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": row['password'],
                "created_at": row['members.created_at'],
                "updated_at": row['members.updated_at']
                }
            adder = member.Member(one_recipes_member_info)
            one_recipe.creator = adder
            recipes.append(one_recipe)
        return recipes

    @classmethod
    def update(cls, data):
        query = "UPDATE recipes SET name = %(name)s, ingredients = %(ingredients)s, instructions = %(instructions)s, under_30 = %(under_30)s, category = %(category)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)


    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)


    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        if len(recipe['name']) < 2:
            is_valid = False
            flash("Name must be at least 3 characters.", 'recipe')
        if len(recipe['ingredients']) < 3:
            is_valid = False
            flash("Ingredients must be at least 3 characters.", 'recipe')
        if len(recipe['instructions']) < 3:
            is_valid = False
            flash("Instructions must be at least 3 characters.", 'recipe')
        return is_valid
