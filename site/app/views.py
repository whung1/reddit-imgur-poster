from app import app, db, login_manager, bcrypt
from app.models import User, Imgur_User, Reddit_User
from flask import render_template, request, redirect, url_for, session, flash
from flask.ext.login import LoginManager, login_required, login_user, logout_user, current_user
import datetime

import app.imgur_backend.imgur_controller as im_control


login_manager.login_view = "login"

@login_manager.user_loader
def user_loader(user_id):
    """Given unicode *user_id*, 
    return the associated User object.
    """
    return User.query.get(int(user_id)) # Primary key is id: int

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    ''' For GET Requests, display login form
    For POSTs, login user by processing form
    '''
    if (request.method == 'GET'):
        # If user is logged in, redirect to home, else show login form
        if('user' in session):
            return redirect(url_for('home'))
        return render_template('login.html', page='login')
    elif (request.method == 'POST'):
        # TODO: Implement User login
        print(request.form)
        user = User.query.filter_by(username=request.form['username']).first()
        if(user is None):
            # TODO: Display message that login failed
            print(User.query.all())
            flash("Username and password combination not found", 'error')
            return render_template('login.html', page='login')
        elif(bcrypt.check_password_hash(user.pwd, request.form['password'])):
            print(user)
            user.authenticated = True
            db.session.add(user)
            db.session.commit()
            if('remember' in request.form):
                login_user(user, remember=True)
            else:
                login_user(user)
            return redirect(url_for('home'))

@app.route('/register/process', methods=['POST'])
def register_process():
    if request.method == 'POST':
        print(request.form)
        # TODO: More Sanitizing of User Registration Input
        # TODO: Error handling if unique != true for username
        if(request.form['confirm-password'] == request.form['password']):
            hashed = bcrypt.generate_password_hash(request.form['password'])
            user = User(username=request.form['username'], pwd=hashed, email=request.form['email'])
            # Register user, log-in, and redirect
            user.authenticated = True
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash("Passwords did not match", 'error')
            return redirect(url_for('login'))

@app.route('/logout')
@login_required
def logout():
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return redirect(url_for('login'))

@app.route('/home')
@login_required
def home():
    return render_template('home.html', page='home')

@app.route('/about')
def about():
    return 'About Page'

@app.route('/contact')
def contact():
    return 'Contact Page'

@app.route('/account')
@login_required
def account():
    # TODO: Delete user
    return "%s's profile" % current_user.username

@app.route('/account/imgur')
@login_required
def imgur_account():
    # TODO: Page to either link or unlink imgur account
    return render_template("imgur_account.html", request_url=im_control.get_request_pin_url())
    
@app.route('/account/imgur/link', methods=['POST'])
@login_required
def imgur_account_link():
    if ('user_pin' in request.form):
        # Exchange for tokens
        response = im_control.exchange_pin_for_tokens(request.form['user_pin'])
        if('success' in response):
            if (response['success'] == True):
                # TODO: Unlink possible remaining imgur_user

                # Create new imgur_user
                im_usr = Imgur_User(username=response['username'],
                        access_token=response['access_token'],
                        refresh_token=response['refresh_token'],
                        user_id=current_user.id)
                db.session.add(im_usr)
                db.session.commit()
                flash("Imgur Account Linked", 'success')
            elif (response['success'] == False):
                flash(response['error'], 'danger')
            return redirect(url_for("imgur_account"))
        else: 
            # Internal error in imgur_backend handling
            return 'Unhandled server error'
        # TODO: Create Imgur_User and bind to current_user account
    else:
        flash("Bad Input", 'danger')
        return redirect(url_for("imgur_account"))

@app.route('/account/imgur/unlink', methods=['POST'])
@login_required
def imgur_account_unlink():
    # TODO: Unbind imgur_user to User
    if ('submit' in request.form):
        im_usr = current_user.imgur_user
        db.session.delete(im_usr)
        db.session.commit()
        flash("Imgur Account Unlinked", "success")
    return redirect(url_for("imgur_account"))

@app.route('/recover')
def recover_account():
    # TODO: Account recovery
    return 'Account Recovery Page'

@app.route('/upload_and_post/process', methods=['POST'])
@login_required
def upload_and_post():
    if(request.method == 'POST'):
        # TODO: Sanitize inputs
        # TODO: Reddit Posting Portion
        response = im_control.basic_img_upload(request.form['img_url'])
        if('success' in response):
            if (response['success'] == True):
                flash(response['imgur_url'], 'success')
            elif (response['success'] == False):
                flash(response['error'], 'danger')
        else: # Internal error in imgur_backend handling
            return 'Unhandled server error'
        return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
