from app import app, db, login_manager, bcrypt, reddit
from app.models import User, Imgur_User, Reddit_User
from flask import render_template, request, redirect, url_for, session, flash
from flask.ext.login import LoginManager, login_required, login_user, logout_user, current_user
from sqlalchemy.exc import IntegrityError

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
            reddit_oauth = r_h.establish_oauth(reddit,
                            current_user.reddit_user)
            return redirect(url_for('home'))

@app.route('/register/process', methods=['POST'])
def register_process():
    if request.method == 'POST':
        # print(request.form)
        # TODO: More Sanitizing of User Registration Input
        # TODO: Error handling if unique != true for username
        if(request.form['confirm-password'] == request.form['password']):
            hashed = bcrypt.generate_password_hash(request.form['password'])
            try:
                user = User(username=request.form['username'], pwd=hashed, email=request.form['email'])
                # Register, log-in, and redirect user
                user.authenticated = True
                db.session.add(user)
                db.session.commit()
                login_user(user)
                return redirect(url_for('home'))
            except IntegrityError:
                flash("That username is taken", "danger")
                return redirect(url_for("login"))
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
    return render_template("account.html",
            page="account",
            in_title = "Account")
            

@app.route('/account/delete', methods=['GET','POST'])
@login_required
def account_delete():
    if (request.method == 'GET'):
        return render_template("account_delete.html",
                page="account_delete",
                in_title="Account | Delete")
    if (request.method == 'POST'):
        # If password confirmation is correct, delete account
        if ('password' in request.form):
            if (bcrypt.check_password_hash(current_user.pwd,
                request.form['password'])):
                # Get from database and delete
                user = User.query.get(current_user.id)
                db.session.delete(user)
                db.session.commit()
                flash("Your account was deleted", "success")
                return redirect(url_for("login"))
            else:
                flash("Password was incorrect", "danger")
        return redirect(url_for("account_delete")) # If fail, redirect to account

@app.route('/account/imgur')
@login_required
def account_imgur():
    if (current_user.imgur_user):
        return render_template("account_imgur_linked.html",
                page="account_imgur_link",
                in_title="Account | Imgur | Linking")
    else:
        return render_template("account_imgur_unlinked.html",
                page="account_imgur_unlink",
                in_title="Account | Imgur | Linking",
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
                print(response)
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
    if (current_user.reddit_user):
        if(r_h.establish_oauth(reddit, current_user.reddit_user)):
            return render_template("account_reddit_linked.html",
                    page="account_reddit_linked",
                    in_title="Account | Reddit | Linking")
        else:
            return "Unhandled error"
    else:
        return render_template('account_reddit_unlinked.html',
                page='account_reddit_unlinked',
                in_title="Account | Reddit | Linking",
                request_url = r_h.get_authorize_url(reddit))

@app.route('/account/reddit/link', methods=['GET'])
@login_required
def account_reddit_link():
    # If an account is linked, unlink before trying to link
    if(current_user.reddit_user is not None):
        account_reddit_unlink()
    # Link the reddit account with the site account
    # print(request.args)
    if ('state' in request.args and 'code' in request.args):
        cur_state = request.args.get('state')
        cur_code = request.args.get('code')
        try:
            info = reddit.get_access_information(cur_code)
        except Exception as e:
            flash("An error occured while linking", "danger")
            return redirect(url_for("account_reddit"))
        if('access_token' in info and 'refresh_token' in info):
            usr = reddit.get_me()
            reddit_usr = Reddit_User(username=usr.name,
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
    if (request.method == 'POST' and
            r_h.establish_oauth(reddit, current_user.reddit_user)):
        # TODO: Sanitize inputs
        print(request.form)
        imgur_response = im_control.image_upload(db, 
                request.form['img_url'], current_user.imgur_user)
        print(imgur_response)
        if ('success' in imgur_response and 
                imgur_response['success'] == True):
            # Image Uploaded
            # Optional comments
            cur_comment = ""
            if ('comment' in request.form):
                cur_comment = request.form['comment']

            args = {'url': imgur_response['imgur_url'],
                    'title': request.form['title'],
                    'subreddit': request.form['subreddit'],
                    'comment': cur_comment}
            link = r_h.submit_post_and_comment(reddit, 
                    current_user.reddit_user,
                    args)
            flash(link, "success")
        elif ('success' not in imgur_response): 
            """Internal coding error or structural
            change in imgur_backend handling"""
            return 'Unhandled server error'
        elif (imgur_response['success'] == False):
            flash(imgur_response['error'], 'danger')
    return redirect(url_for("home")) # Always redirect back to home

