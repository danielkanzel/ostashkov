import os
from flask import Flask, request, render_template, redirect, url_for, session, flash, abort
from flask_sqlalchemy import SQLAlchemy

# Flask config
app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

from models import *

@app.route('/')
def home():
    title = "Карта славного города Осташкова"
    map_apikey = app.config['YANDEX_APIKEY']
    login_url = url_for("login")
    return render_template("home.html",title=title, map_apikey=map_apikey, login_url=login_url)

@app.route('/placemark.js')
def placemark():
    markers_list = []
    for c in Place.query.all():
        markers_list.append(c.__dict__)
    for i in markers_list:
        i["place_url"] = url_for("place", id=i["id"])
    return render_template('placemark.js', markers_list=markers_list)

@app.route('/place/<id>')
def place(id):
    place_dict = {}
    for c in Place.query.filter_by(id=id):
        place_dict=dict(c.__dict__)
    if place_dict.get("name") == None:
        abort(404)
    return render_template("place.html",
                            name=place_dict.get("name"),
                            address=place_dict.get("address"),
                            description=place_dict.get("description"),
                            image_url=place_dict.get("image_url"))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('logged_in'):
        return redirect(url_for("admin"))
    error = None
    users_list = []
    if request.method == 'POST':
        for c in User.query.all():
            users_list.append(c.__dict__)
        if not any(user.get('username') == request.form['username'] for user in users_list):
            error = 'Invalid username'
        elif not any(user.get('password') == request.form['password'] for user in users_list):
            error = 'Invalid password'     
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for("admin"))
    return render_template("login.html",error=error)

@app.route('/logout')
def logout():
    if not session.get('logged_in'):
        abort(401)
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(request.url_root)


@app.route('/admin')
def admin():
    if not session.get('logged_in'):
        abort(401)
    places_list = []
    for c in Place.query.all():
        places_list.append(c.__dict__)
    return render_template("admin.html",places_list=places_list)

@app.route('/add_place',  methods=['GET', 'POST'])
def add_place():
    if not session.get('logged_in'):
        abort(401)
    error = None
    map_apikey = app.config['YANDEX_APIKEY']
    if request.method == 'POST':
        if len(request.form['name']) > 120:
            error = 'Too large title'
        else:
            db.session.add(Place(
                name=request.form['name'],
                image_url=request.form['image_url'],
                address=request.form['address'],
                description=request.form['description'],
                longitude=request.form['longitude'],
                latitude=request.form['latitude']
                ))
            db.session.commit()
            flash('Place added')
            return redirect(url_for('admin'))
    return render_template('add_place.html', error=error, map_apikey=map_apikey)

@app.route('/coordinates.js')
def coordinates():
    return render_template("coordinates.js")

@app.route('/remove_place/<id>')
def remove_place(id):
    if not session.get('logged_in'):
        abort(401)
    Place.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    error = None
    users_list = []
    if request.method == 'POST':
        for c in User.query.all():
            users_list.append(c.__dict__)
        if any(user.get('username') == request.form['username'] for user in users_list):
            error = 'User existed'    
        else:
            db.session.add(User(
                username=request.form['username'],
                password=request.form['password']
                ))
            db.session.commit()
            flash('User added')
            return redirect(url_for('admin'))
    return render_template('add_user.html', error=error)




# Run by file
if __name__ == "__main__":
    app.debug = True
    app.run()