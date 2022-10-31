from flask_login import current_user
from app import app
from flask import render_template, flash, redirect, url_for
from .models import User, Product

@app.route('/')
def homePage():
    # users = User.query.all()

    # cart_set = dict()
    # for u in users:
    #     my_cart = u.my_team.all()
    #     print(my_cart)
    #     cart_set[u.username] = my_cart
      
    return render_template('index.html')

@app.route('/login')
def loginPage():
    return render_template('login.html')

