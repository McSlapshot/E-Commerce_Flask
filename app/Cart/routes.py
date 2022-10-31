from flask import Blueprint, render_template, request, url_for, redirect
from flask_login import login_required, current_user
from app.models  import myCart
from .forms import CreateCart

cart = Blueprint('cart', __name__, template_folder='cart_templates')

@cart.route('/carts/create_cart', methods=["GET", "POST"])
@login_required
def createCart():
    form = CreateCart()
    if request.method == "POST":
        if form.validate():
            cart_name = form.cart_name.data
            img_url = form.img_url.data
            caption = form.caption.data

            cart = myCart(cart_name, img_url, caption, current_user.id)

            cart.saveToDB()

            return redirect(url_for('homePage'))

    return render_template('create_cart.html', form=form)

@cart.route('/carts')
def viewCarts():
    carts = myCart.query.order_by(myCart.date_created).all()[::-1]
    return render_template('team.html', carts=carts)