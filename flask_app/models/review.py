from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import member

class Review:
    db_name = 'podcast_postings_schema'
    def __init__(self, data):
        self.id = data['id']
        self.review_title = data['review_title']
        self.podcast_name = data['podcast_name']
        self.category = data['category']
        self.host = data['host']
        self.stars = data['stars']
        self.review_text = data['review_text']
        self.member_id = data['member_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None

    @classmethod
    def create(cls, data):
        query = "INSERT INTO reviews (review_title, podcast_name, category, host, stars, review_text, member_id) VALUES (%(review_title)s, %(podcast_name)s, %(category)s, %(host)s, %(stars)s, %(review_text)s, %(member_id)s);"
        return connectToMySQL(cls.db_name).query_db(query,data)


    @classmethod
    def get_all(cls):
        query = "SELECT * FROM reviews;"
        result = connectToMySQL(cls.db_name).query_db(query)
        all_reviews = []
        for row in result:
            all_reviews.append( cls(row) )
        return all_reviews

    @classmethod
    def get_all_reviews_with_member(cls):
        query = "SELECT * FROM reviews JOIN members ON reviews.member_id = members.id;"
        results = connectToMySQL(cls.db_name).query_db(query)
        reviews = []
        for row in results:
            one_review = cls(row)
            one_reviews_member_info = {
                "id": row['members.id'], 
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": row['password'],
                "created_at": row['members.created_at'],
                "updated_at": row['members.updated_at']
                }
            adder = member.Member(one_reviews_member_info)
            one_review.creator = adder
            reviews.append(one_review)
        return reviews


    @classmethod
    def get_all_reviews_from_one_member(cls, data):
        query = "SELECT * FROM reviews JOIN members ON reviews.member_id = members.id WHERE member_id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        reviews = []
        for row in results:
            one_review = cls(row)
            one_reviews_member_info = {
                "id": row['members.id'], 
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": row['password'],
                "created_at": row['members.created_at'],
                "updated_at": row['members.updated_at']
                }
            adder = member.Member(one_reviews_member_info)
            one_review.creator = adder
            reviews.append(one_review)
        return reviews

    @classmethod
    def get_one_review_with_member(cls, data):
        query = "SELECT * FROM reviews JOIN members ON reviews.member_id = members.id WHERE reviews.id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        one_review = cls(results[0])
        one_reviews_member_info = {
            "id": results[0]['members.id'], 
            "first_name": results[0]['first_name'],
            "last_name": results[0]['last_name'],
            "email": results[0]['email'],
            "password": results[0]['password'],
            "created_at": results[0]['members.created_at'],
            "updated_at": results[0]['members.updated_at']
            }
        adder = member.Member(one_reviews_member_info)
        one_review.creator = adder
        return one_review

    @classmethod
    def get_review_by_id(cls,data):
        query = "SELECT * FROM reviews WHERE id = %(id)s;"
        result = connectToMySQL(cls.db_name).query_db(query,data)
        return cls(result[0])

    @classmethod
    def get_all_reviews_from_category(cls, data):
        query = "SELECT * FROM reviews JOIN members ON reviews.member_id = members.id WHERE category = %(category)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        reviews = []
        for row in results:
            one_review = cls(row)
            one_reviews_member_info = {
                "id": row['members.id'], 
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": row['password'],
                "created_at": row['members.created_at'],
                "updated_at": row['members.updated_at']
                }
            adder = member.Member(one_reviews_member_info)
            one_review.creator = adder
            reviews.append(one_review)
        return reviews

    @classmethod
    def get_all_reviews_from_under_30(cls, data):
        query = "SELECT * FROM reviews JOIN members ON reviews.member_id = members.id WHERE under_30 = %(under_30)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        reviews = []
        for row in results:
            one_review = cls(row)
            one_reviews_member_info = {
                "id": row['members.id'], 
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": row['password'],
                "created_at": row['members.created_at'],
                "updated_at": row['members.updated_at']
                }
            adder = member.Member(one_reviews_member_info)
            one_review.creator = adder
            reviews.append(one_review)
        return reviews

    @classmethod
    def update(cls, data):
        query = "UPDATE reviews SET review_title = %(review_title)s, podcast_name = %(podcast_name)s, category = %(category)s, host = %(host)s, stars = %(stars)s, review_text = %(review_text)s, updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)


    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM reviews WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)


    @staticmethod
    def validate_review(review):
        is_valid = True
        if len(review['review_title']) < 2:
            is_valid = False
            flash("Review Title must be at least 2 characters.", 'review')
        if len(review['podcast_name']) < 2:
            is_valid = False
            flash("Podcast Name must be at least 2 characters.", 'review')
        if len(review['host']) < 2:
            is_valid = False
            flash("Host(s) must be at least 2 characters.", 'review')
        if len(review['review_text']) < 3:
            is_valid = False
            flash("Review must be at least 3 characters.", 'review')
        return is_valid