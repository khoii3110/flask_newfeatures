from market import app
from flask import render_template, redirect, url_for, flash, request
from market.models import Item, User
from market.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm
from market import db
from flask_login import login_user, logout_user, login_required, current_user
from market.forms import UpdateProfileForm  # Import the new form

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/market', methods=['GET', 'POST'])
@login_required
def market_page():
    purchase_form = PurchaseItemForm()
    selling_form = SellItemForm()

    # Handle purchase and sell actions as you already did
    if request.method == "POST":
        # Purchase Item Logic
        purchased_item = request.form.get('purchased_item')
        p_item_object = Item.query.filter_by(name=purchased_item).first()
        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                flash(f"Congratulations! You purchased {p_item_object.name} for {p_item_object.price}$", category='success')
            else:
                flash(f"Unfortunately, you don't have enough money to purchase {p_item_object.name}!", category='danger')

        # Sell Item Logic
        sold_item = request.form.get('sold_item')
        s_item_object = Item.query.filter_by(name=sold_item).first()
        if s_item_object:
            if current_user.can_sell(s_item_object):
                s_item_object.sell(current_user)
                flash(f"Congratulations! You sold {s_item_object.name} back to market!", category='success')
            else:
                flash(f"Something went wrong with selling {s_item_object.name}", category='danger')

        return redirect(url_for('market_page'))

    if request.method == "GET":
        # Get filter parameters from request
        search_query = request.args.get('search', '')
        category = request.args.get('category', '')
        min_price = request.args.get('min_price', type=int)
        max_price = request.args.get('max_price', type=int)

        # Start with the query for items that don't have an owner (i.e., available for purchase)
        items = Item.query.filter_by(owner=None)

        # Apply filters if applicable
        if search_query:
            items = items.filter(Item.name.ilike(f'%{search_query}%'))
        if category:
            items = items.filter(Item.category == category)
        if min_price is not None:
            items = items.filter(Item.price >= min_price)
        if max_price is not None:
            items = items.filter(Item.price <= max_price)

        items = items.all()  # Execute the query

        # Get the current user's owned items
        owned_items = Item.query.filter_by(owner=current_user.id)

        # Return the market page with the filtered items and the owned items
        return render_template('market.html', items=items, purchase_form=purchase_form, owned_items=owned_items, selling_form=selling_form)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Account created successfully! You are now logged in as {user_to_create.username}", category='success')
        return redirect(url_for('market_page'))
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('market_page'))
        else:
            flash('Username and password are not match! Please try again', category='danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))


from market.forms import UpdateProfileForm  # Import the new form

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile_page():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email_address = form.email_address.data
        if form.password.data:
            current_user.password = form.password.data
        db.session.commit()
        flash("Your profile has been updated!", category='success')
        return redirect(url_for('profile_page'))
    
    # Populate the form with the current user info on GET request
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email_address.data = current_user.email_address

    return render_template('profile.html', form=form)

from market.models import Wishlist

@app.route('/wishlist')
@login_required
def wishlist_page():
    wishlist_items = Wishlist.query.filter_by(user_id=current_user.id).all()
    print(wishlist_items)  # Debugging line
    items = [wishlist_item.item for wishlist_item in wishlist_items]
    return render_template('wishlist.html', items=items)




@app.route('/add_to_wishlist/<int:item_id>', methods=['POST'])
@login_required
def add_to_wishlist(item_id):
    item = Item.query.get(item_id)
    if item:
        # Check if the item is already in the wishlist
        if Wishlist.query.filter_by(user_id=current_user.id, item_id=item_id).first() is None:
            wishlist_entry = Wishlist(user_id=current_user.id, item_id=item_id)
            db.session.add(wishlist_entry)
            db.session.commit()
            flash(f'{item.name} added to your wishlist!', 'success')
        else:
            flash(f'{item.name} is already in your wishlist.', 'info')
    return redirect(url_for('market_page'))


@app.route('/remove_from_wishlist/<int:item_id>', methods=['POST'])
@login_required
def remove_from_wishlist(item_id):
    wishlist_entry = Wishlist.query.filter_by(user_id=current_user.id, item_id=item_id).first()
    if wishlist_entry:
        db.session.delete(wishlist_entry)
        db.session.commit()
        flash(f'Item removed from wishlist.', 'info')
    return redirect(url_for('wishlist_page'))  # Ensure redirect to wishlist page








