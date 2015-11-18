from app import app, db, login_manager, bcrypt
from app.models import User
from flask import render_template, request, redirect, url_for, session
from flask.ext.login import LoginManager, login_required, login_user, logout_user, current_user
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
            print("fail")
            return render_template('login.html', page='login')
        elif(bcrypt.check_password_hash(user.password, request.form['password'])):
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
            # Automatically log-in and redirect
            user.authenticated = True
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('home'))
        else:
            return 'Confirmed password was not the same as password'

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

@app.route('/user/<username>')
@login_required
def show_user_profile():
    # TODO: Delete user
    return "%s's profile" % current_user.username

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
            if(response['success'] == True):
                return redirect(response['imgur_link'])
            else: # Image did not upload
                # TODO: Meaningful error message
                return 'Image upload failed'
        else: # Internal error in imgur_backend handling
            return 'Unhandled server error'


if __name__ == "__main__":
    app.run(debug=True)
