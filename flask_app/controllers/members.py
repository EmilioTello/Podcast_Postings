from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.member import Member
from flask_app.models.recipe import Recipe
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    if not Member.validate_register(request.form):
        return redirect('/')
    data ={
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = Member.create(data)
    session['member_id'] = id
    return redirect('/dashboard')


@app.route('/login', methods=['POST'])
def login():
    member = Member.get_one_by_email(request.form)
    if not member:
        flash("Invalid email/password.", 'login')
        return redirect('/')
    if not bcrypt.check_password_hash(member.password, request.form['password']):
        flash("Invalid email/password.", 'login')
        return redirect('/')
    session['member_id'] = member.id
    return redirect('/dashboard')
    

@app.route('/dashboard')
def dashboard():
    if 'member_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['member_id']
    }
    return render_template('dashboard.html', member = Member.get_one_by_id(data), recipes=Recipe.get_all_recipes_with_member())


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')