from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.recipe import Recipe
from flask_app.models.member import Member


@app.route('/recipe/new')
def new_recipe():
    if 'member_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['member_id']
    }
    return render_template('new_recipe.html', member=Member.get_one_by_id(data))


@app.route('/recipe/create', methods=['POST'])
def create_recipe():
    if 'member_id' not in session:
        return redirect('/logout')
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipe/new')
    data = {
        "name": request.form['name'],
        "ingredients": request.form['ingredients'],
        "instructions": request.form['instructions'],
        "under_30": int(request.form['under_30']),
        "category": request.form['category'],
        "member_id": session["member_id"]
    }
    Recipe.create(data)
    return redirect('/dashboard')

@app.route('/recipe/edit/<int:id>')
def edit_recipe(id):
    if 'member_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    member_data = {
        "id":session['member_id']
    }
    return render_template("edit_recipe.html",edit=Recipe.get_recipe_by_id(data),member=Member.get_one_by_id(member_data))


@app.route('/recipe/update',methods=['POST'])
def update_recipe():
    if 'member_id' not in session:
        return redirect('/logout')
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipe/new')
    data = {
        "name": request.form["name"],
        "ingredients": request.form["ingredients"],
        "instructions": request.form["instructions"],
        "under_30": int(request.form["under_30"]),
        "category": request.form['category'],
        "id": request.form["id"]
    }
    Recipe.update(data)
    return redirect('/dashboard')

@app.route('/recipe/<int:id>')
def recipe(id):
    if 'member_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    member_data = {
        "id":session['member_id']
    }
    return render_template("show_recipe.html",recipe=Recipe.get_one_recipe_with_member(data),member=Member.get_one_by_id(member_data))

@app.route('/recipe/destroy/<int:id>')
def destroy_recipe(id):
    if 'member_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Recipe.destroy(data)
    return redirect('/dashboard')

@app.route('/recipes/<string:category>')
def category(category):
    if 'member_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['member_id']
    }
    data_two = {
        "category": category
    }
    return render_template('category.html', member=Member.get_one_by_id(data), recipes=Recipe.get_all_recipes_from_category(data_two))

@app.route('/recipes/<int:under_30>')
def under_30(under_30):
    if 'member_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['member_id']
    }
    data_two = {
        "under_30": under_30
    }
    return render_template('under_30.html', member=Member.get_one_by_id(data), recipes=Recipe.get_all_recipes_from_under_30(data_two))

@app.route('/member/<int:id>')
def member_recipes(id):
    if 'member_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    member_data={
        'id': session['member_id']
    }
    return render_template('member_recipes.html', member = Member.get_one_by_id(member_data), recipes=Recipe.get_all_recipes_from_one_member(data), adder = Member.get_one_by_id(data))