from app import app, db, login_manager, bcrypt, reddit
from app.models import User, Imgur_User, Reddit_User
from flask import render_template, request, redirect, url_for, session, flash
from flask.ext.login import LoginManager, login_required, login_user, logout_user, current_user
import datetime

import app.imgur_backend.imgur_controller as im_control
import app.reddit_backend.reddit_helper as r_h

# TODO: Unique instance of Reddit Object per user

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
    # If user is logged in, redirect to home immediately
    if(current_user.is_active):
        return redirect(url_for('home'))
    # Otherwise, handle GET and POST normally
    if (request.method == 'GET'):
        return render_template('login.html', page='login')
    elif (request.method == 'POST'):
        user = User.query.filter_by(username=request.form['username']).first()
        if(user is None):
            flash("Username and password combination not found", 'error')
            return redirect(url_for("login"))
        elif(bcrypt.check_password_hash(user.pwd, request.form['password'])):
            user.authenticated = True
            db.session.add(user)
            db.session.commit()
            remember_login=False
            if('remember' in request.form):
                remember_login=True
            login_user(user, remember=remember_login)
            # Re-establish OAuth for reddit object if it exists
            reddit_oauth = r_h.reestablish_oauth(reddit,
                            current_user.reddit_user)
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
            # Register, log-in, and redirect user
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
    if(user):
        user.authenticated = False
        db.session.add(user)
        db.session.commit()
        logout_user()
    return redirect(url_for('login'))

@app.route('/home')
@login_required
def home():
    return render_template('home.html',
            page='home',
            in_title = "Home")

@app.route('/about')
def about():
    return 'About Page'

@app.route('/contact')
def contact():
    return 'Contact Page'

@app.route('/recover')
def recover_account():
    # TODO: Account recovery
    return 'Account Recovery Page'

@app.route('/account')
@login_required
def account():
    # TODO: Delete user
    # TODO: Account page
    return "%s's profile" % current_user.username

@app.route('/account/imgur')
@login_required
def account_imgur():
    return render_template("account_imgur.html",
            page="account_imgur",
            in_title="Account | Imgur",
            request_url=im_control.get_request_pin_url())
    
@app.route('/account/imgur/link', methods=['POST'])
@login_required
def account_imgur_link():
    if ('user_pin' in request.form):
        # Check if current_user has existing Imgur account
        im_usr = Imgur_User.query.filter_by(user_id=current_user.id).first()
        if(im_usr):
            # There is existing account, stop and return
            flash("There is an Imgur account already linked to your current account", "danger")
            return redirect(url_for("account_imgur"))
        # There is no account linked, continue to try to link
        response = im_control.exchange_pin_for_tokens(request.form['user_pin'])
        if('success' in response):
            if (response['success'] == True):
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
            return redirect(url_for("account_imgur"))
        else: 
            # Internal error in imgur_backend handling
            return 'Unhandled server error'
    else:
        flash("Bad Input", 'danger')
        return redirect(url_for("account_imgur"))

@app.route('/account/imgur/unlink', methods=['POST'])
@login_required
def account_imgur_unlink():
    # Remove Imgur_User from database
    if ('submit' in request.form):
        im_usr = current_user.imgur_user
        if(im_usr):
            db.session.delete(im_usr)
            db.session.commit()
            flash("Imgur Account Unlinked", "warning")
        else:
            flash("Imgur account not found", "danger")
    return redirect(url_for("account_imgur"))

@app.route('/account/reddit')
@login_required
def account_reddit():
    return render_template('account_reddit.html',
            page='account_reddit',
            in_title="Account | Reddit",
            request_url = r_h.get_authorize_url(reddit))

@app.route('/account/reddit/link', methods=['GET'])
@login_required
def account_reddit_link():
    print(request.args)
    if ('state' in request.args and 'code' in request.args):
        cur_state = request.args.get('state')
        # TODO: Check states
        cur_code = request.args.get('code')
        # TODO: Fail get_access_information gracefully
        # TODO: Unlink before relink
        info = reddit.get_access_information(cur_code)
        if('access_token' in info and 'refresh_token' in info):
            usr = reddit.get_me()
            reddit_usr = Reddit_User(username=usr.name,
                        access_token=info['access_token'],
                        refresh_token=info['refresh_token'],
                        user_id=current_user.id)
            db.session.add(reddit_usr)
            db.session.commit()
            flash("Reddit Account Linked", 'success')
            return redirect(url_for('account_reddit'))
    else:
        return redirect(url_for('account_reddit'))

@app.route('/account/reddit/unlink', methods=['POST'])
@login_required
def account_reddit_unlink():
    # Delete Reddit_User from database
    if ('submit' in request.form):
        reddit_usr = current_user.reddit_user
        if (reddit_usr):
            reddit.clear_authentication()
            db.session.delete(reddit_usr)
            db.session.commit()
            flash("Reddit Account Unlinked", "warning")
        else:
            flash("Reddit Account Not Found", "danger")
    return redirect(url_for("account_reddit"))

@app.route('/upload_and_post/process', methods=['POST'])
@login_required
def upload_and_post():
    if(request.method == 'POST'):
        # TODO: Sanitize inputs
        response = im_control.image_upload(current_user.imgur_user, request.form['img_url'])
        if('success' in response):
            if (response['success'] == True):
                # Image Uploaded
                flash(response['imgur_url'], 'success')
                # TODO: Reddit Posting and Commenting Portion
                # TODO: Captcha Handling
            elif (response['success'] == False):
                flash(response['error'], 'danger')
        else: # Internal error in imgur_backend handling
            return 'Unhandled server error'
        return redirect(url_for("home"))

