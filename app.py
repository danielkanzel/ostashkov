import os
from flask import Flask, request, render_template, redirect, url_for, session, flash, abort
from flask_sqlalchemy import SQLAlchemy

# Flask config
app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(64), index=True, unique=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User %r>' % (self.nickname)

    def serialize(self):
        return {
            'id': self.id, 
            'username': self.name,
            'password': self.author
        }

class Place(db.Model):
    __tablename__ = 'places'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True, unique=False)
    address = db.Column(db.String(250), index=True, unique=False)
    image_url = db.Column(db.String(250), index=True, unique=False) 
    description = db.Column(db.String(6400), index=True, unique=False)
    longitude = db.Column(db.String(12), index=True, unique=False)
    latitude = db.Column(db.String(12), index=True, unique=False)

    def __init__(self, name, address,image_url,description,longitude,latitude):
        self.name = name
        self.address = address
        self.image_url = image_url
        self.description = description
        self.longitude = longitude
        self.latitude = latitude

    def __repr__(self):
        return '<Place %r>' % (self.title)
    
    def serialize(self):
        return {
            'id': self.id, 
            'name': self.name,
            'address': self.author,
            'image_url': self.image_url,
            'description': self.description,
            'longitude': self.longitude,
            'latitude': self.latitude
        }

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
    return render_template('placemark.js', markers_list=markers_list)

@app.route('/place/<id>')
def place(id):
    place_dict = {}
    for c in Place.query.filter_by(id=id):
        place_dict=dict(c.__dict__)
    return render_template("place.html",
                            name=place_dict.get("name"),
                            address=place_dict.get("address"),
                            description=place_dict.get("description"),
                            image_url=place_dict.get("image_url"))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    users_list = []
    if request.method == 'POST':
        for c in Place.query.all():
            users_list.append(c.__dict__)
        for user in users_list:
            if user['username'] == request.form['username']:
                if user['password'] == request.form['password']:
                    return True
                else:
                    error = 'Invalid password'
            else: 
                error = 'Invalid username'
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
    return render_template('add_place.html', error=error)

@app.route('/remove_place/<id>')
def remove_place(id):
    if not session.get('logged_in'):
        abort(401)
    Place.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/add_user')
def add_user():
    db.session.add(User(
        username=request.args.get('username'),
        password=request.args.get('password')
        ))
    db.session.commit()
    flash('User added')
    return "done"


# Run by file
if __name__ == "__main__":
    app.debug = True
    app.run()