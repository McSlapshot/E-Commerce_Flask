from flask import Blueprint, render_template, request, url_for, redirect, flash
from flask_login import login_fresh, login_required, current_user
from app.models  import Product, myCart
from .forms import CreatePostForm
import requests, json

product = Blueprint('product', __name__, template_folder='product_templates')

@product.route('/product/add', methods=["GET", "POST"])
@login_required
def searchProduct():
    form = CreatePostForm()
    if request.method == "POST":
        if form.validate():
            item = form.item.data
            url = f'https://botw-compendium.herokuapp.com/api/v2/entry/{item}'
            requests.get(url)
            response = requests.get(url)
            if response.ok:
                product_dict = {}
                data =  response.json()
                product_dict[item.title()] = {
                    'name': data['data']['name'],
                    'id': data['data']['id'],
                    'img_url': data['data']['image'],
                    'description': data['data']['description']
            }

                name = product_dict[item.title()]['name']
                item_id = product_dict[item.title()]['id']
                img_url = product_dict[item.title()]['image']
                description = product_dict[item.title()]['description']
            else:
                flash('That item does not exist', 'danger')
                return redirect(url_for('product.searchProduct'))
            
            u1 = myCart.query.filter_by(item=item).first()
            if u1:
                flash('Product already exists in the shop', 'danger')
            else:
                flash(f'Succesfully added {item} to the shop!', 'success')
                product = Product(item, name, img_url, item_id, description, current_user.id)
                product.saveToDB()
                

    return render_template('search.html', form=form)

@product.route('/product')
def viewProduct():
    products = Product.query.order_by(Product.name).all()[::-1]
    return render_template('items.html', products=products)

@product.route('/add_to_cart/<int:product_id>')
@login_required
def addCart(product_id):
    product = Product.query.get(product_id)
    if product:
        # print(current_user.pokemon_team.count())
        if current_user.my_cart.count() == 5:
            flash('cart full', 'danger')
        else:
            current_user.addToCart(product)
            flash(f'Successfully added {product.name} to {current_user.username}\'s team', 'success')
    else:
        flash(f'Cannot add product that does not exist...', 'danger')
    return redirect(url_for('homePage'))

@product.route('/remove_from_cart/<int:product_id>')
@login_required
def removeCart(product_id):
    product = Product.query.get(product_id)
    if product:
        p = Product.query.filter_by(product_id=product.id).first()
        current_user.removeFromCart(p)
        flash(f'Successfully removed {product.name} from {current_user.username}\'s cart', 'success')
    else:
        flash(f'Cannot remove product that does not exist...', 'danger')

    return redirect(url_for('homePage'))

