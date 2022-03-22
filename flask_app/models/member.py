from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.recipe import Recipe
import re


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Member:
    db_name = 'family_cookbook_schema'
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.recipes = []

    @classmethod
    def create(cls, data):
        query = "INSERT INTO members (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        result = connectToMySQL(cls.db_name).query_db(query,data)
        return result

    @classmethod
    def get_one_by_id(cls,data):
        query = "SELECT * FROM members WHERE id = %(id)s;"
        result = connectToMySQL(cls.db_name).query_db(query,data)
        return cls(result[0])

    @classmethod
    def get_one_by_email(cls,data):
        query = "SELECT * FROM members WHERE email = %(email)s;"
        result = connectToMySQL(cls.db_name).query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])


    @staticmethod
    def validate_register(member):
        is_valid = True
        if len(member['first_name']) < 2:
            is_valid = False
            flash("First name must be at least 2 characters.", 'register')
        elif not member['first_name'].isalpha():
            is_valid = False
            flash("First name can contain letters only.", 'register')
        if len(member['last_name']) < 2:
            is_valid = False
            flash("Last name must be at least 2 characters.", 'register')
        elif not member['last_name'].isalpha():
            is_valid = False
            flash("Last name can contain letters only.", 'register')
        query = "SELECT * FROM members WHERE email = %(email)s;"
        result = connectToMySQL(Member.db_name).query_db(query, member)
        if len(result) >= 1:
            is_valid=False
            flash("Email Already Taken!", 'register')
        elif not EMAIL_REGEX.match(member['email']):
            is_valid = False
            flash("Email is not in valid format, e.g., name@company.com", 'register')
        if len(member['password']) < 8:
            is_valid = False
            flash("Password must be at least 8 characters.", 'register')
        if member['confirm_password'] != member['password']:
            is_valid = False
            flash("Confirm password must match password.", 'register')
        return is_valid
