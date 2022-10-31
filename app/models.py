from itertools import product
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash

db = SQLAlchemy()

the_cart = db.Table(
    'cart',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), nullable=False),
    db.Column('pokemon_id', db.Integer, db.ForeignKey('product.id'), nullable=False)
)

class myCart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(250), nullable=False)
    post = db.relationship("Post", cascade="all, delete", backref='author', lazy=True)
    product = db.relationship("Product", cascade="all,delete", backref='author', lazy=True)
    person = db.relationship("Product",
        secondary = the_cart,
        backref= db.backref('person', lazy='dynamic'),
        lazy='dynamic'
    )
    my_cart = db.relationship("Product",
        secondary = "mycart",
        backref= db.backref('person2', lazy='dynamic'),
        lazy='dynamic'
    )

    def __init__(self, username, first_name, last_name, email, password):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = generate_password_hash(password)

    def saveToDB(self):
        db.session.add(self)
        db.session.commit()

    def deleteFromDB(self):
        db.session.delete(self)
        db.session.commit()

    def saveChanges(self):
        db.session.commit()

    def addToCart(self, product):
        self.my_cart.append(product)
        db.session.commit()

    def removeFromCart(self, p):
        # p is expected to be a product instance
        db.session.delete(p)
        db.session.commit()

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    img_url = db.Column(db.String)
    caption = db.Column(db.String(300))
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, title, img_url, caption, user_id):
        self.title = title
        self.img_url = img_url
        self.caption = caption
        self.user_id = user_id

    def saveToDB(self):
        db.session.add(self)
        db.session.commit()

    def deleteFromDB(self):
        db.session.delete(self)
        db.session.commit()

    def saveChanges(self):
        db.session.commit()

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    item_id = db.Column(db.Integer)
    img_url = db.Column(db.String)
    description = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, name, item_id, img_url, description, user_id):
        self.name = name
        self.item_id = item_id
        self.img_url = img_url
        self.description = description
        self.user_id = user_id

    def saveToDB(self):
        db.session.add(self)
        db.session.commit()