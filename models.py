
from app import db


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
