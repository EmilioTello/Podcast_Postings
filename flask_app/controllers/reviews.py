from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.review import Review
from flask_app.models.member import Member
from listennotes import podcast_api


@app.route('/review/new')
def new_review():
    if 'member_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['member_id']
    }
    return render_template('new_review.html', member=Member.get_one_by_id(data))


@app.route('/review/create', methods=['POST'])
def create_review():
    if 'member_id' not in session:
        return redirect('/logout')
    if not Review.validate_review(request.form):
        return redirect('/review/new')
    data = {
        "review_title": request.form['review_title'],
        "podcast_name": request.form['podcast_name'],
        "category": (request.form['category']),
        "host": request.form['host'],
        "stars": request.form['stars'],
        "review_text": request.form['review_text'],
        "member_id": session["member_id"]
    }
    Review.create(data)
    return redirect('/dashboard')

@app.route('/review/edit/<int:id>')
def edit_review(id):
    if 'member_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    member_data = {
        "id":session['member_id']
    }
    return render_template("edit_review.html",edit=Review.get_review_by_id(data),member=Member.get_one_by_id(member_data))


@app.route('/review/update',methods=['POST'])
def update_review():
    if 'member_id' not in session:
        return redirect('/logout')
    if not Review.validate_review(request.form):
        return redirect('/review/new')
    data = {
        "review_title": request.form['review_title'],
        "podcast_name": request.form['podcast_name'],
        "category": (request.form['category']),
        "host": request.form['host'],
        "stars": request.form['stars'],
        "review_text": request.form['review_text'],
        "id": request.form["id"]
    }
    Review.update(data)
    return redirect('/dashboard')

@app.route('/review/<int:id>')
def review(id):
    if 'member_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    member_data = {
        "id":session['member_id']
    }
    return render_template("show_review.html",review=Review.get_one_review_with_member(data),member=Member.get_one_by_id(member_data))

@app.route('/review/destroy/<int:id>')
def destroy_review(id):
    if 'member_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Review.destroy(data)
    return redirect('/dashboard')

@app.route('/reviews/<string:category>')
def category(category):
    if 'member_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['member_id']
    }
    data_two = {
        "category": category
    }
    return render_template('category.html', member=Member.get_one_by_id(data), reviews=Review.get_all_reviews_from_category(data_two))

@app.route('/reviews/for_<string:podcast_name>')
def podcast_name(podcast_name):
    if 'member_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['member_id']
    }
    data_two = {
        "podcast_name": podcast_name
    }
    return render_template('podcast_name.html', member=Member.get_one_by_id(data), reviews=Review.get_all_reviews_from_podcast_name(data_two))

@app.route('/reviews/hosted_by_<string:host>')
def host(host):
    if 'member_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['member_id']
    }
    data_two = {
        "host": host
    }
    return render_template('host.html', member=Member.get_one_by_id(data), reviews=Review.get_all_reviews_from_host(data_two))

@app.route('/reviews/by_<int:stars>')
def stars(stars):
    if 'member_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['member_id']
    }
    data_two = {
        "stars": stars
    }
    return render_template('stars.html', member=Member.get_one_by_id(data), reviews=Review.get_all_reviews_from_stars(data_two))


@app.route('/member/<int:id>')
def member_reviews(id):
    if 'member_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    member_data={
        'id': session['member_id']
    }
    return render_template('member_reviews.html', member = Member.get_one_by_id(member_data), reviews=Review.get_all_reviews_from_one_member(data), adder = Member.get_one_by_id(data))

@app.route('/listen')
def randomPodcast():
    client = podcast_api.Client(api_key=None) # api-key to be added at future time, 'None' api_key is used for testing purposes
    response = client.just_listen()
    data = response.json()
    randomPodcastData = {
        'id' : data['id'],
        'title' : data['title'],
        'audio' : data['audio'],
        'thumbnail' : data['thumbnail'],
        'description' : data['description'],
        'listenNotesURL' : data['listennotes_url']
    }
    member_data={
        'id': session['member_id']
    }
    return render_template('listen.html', member = Member.get_one_by_id(member_data), randomPodcastData=randomPodcastData)