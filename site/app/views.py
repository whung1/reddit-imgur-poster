from app import app, db, models
from flask import render_template, request, redirect, url_for, session
import app.imgur_backend.imgur_controller as im_control 

@app.route('/')
@app.route('/login')
def login():
    if('user' in session):
        return redirect(url_for('home'))
    return render_template('login.html', page='login')

@app.route('/login/process', methods=['GET', 'POST'])
def login_process(username=None, password=None):
    if request.method == 'POST':
        # TODO: Implement User login
        print(request.form)
        user = models.User.query.filter_by(username=request.form['username'], pwd=request.form['password']).first_or_404()
        session['user'] = user.username
        return redirect(url_for('home'))
    elif (request.method == 'GET' and username != None):
        # Special login after the first time user registers
        user = models.User.query.filter_by(username=username, pwd=password).first_or_404()
        session['user'] = user.username
        return redirect(url_for('home'))

@app.route('/register/process', methods=['POST'])
def register_process():
    if request.method == 'POST':
        print(request.form)
        # TODO: More Sanitizing of User Registration Input
        # TODO: Error handling if unique != true for username or email
        if(request.form['confirm-password'] == request.form['password']):
            u = models.User(username=request.form['username'], pwd=request.form['password'], email=request.form['email'])
            db.session.add(u)
            db.session.commit()
            users = models.User.query.all()
            print(users)
            return 'Registration successful'
            # TODO: Automatically log-in and redirect
            #return redirect(url_for('login_process', username=u.username, password=u.pwd)) # Extremely unsafe unencrypted
        else:
            return 'Confirmed password was not the same as password'

@app.route('/home')
def home():
    if('user' not in session):
        return redirect(url_for('login'))
    else:
        return render_template('home.html', page='home')

@app.route('/upload_and_post/process', methods=['POST'])
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

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/about')
def about():
    return 'About Page'

@app.route('/contact')
def contact():
    return 'Contact Page'

@app.route('/user/<username>')
def show_user_profile(username):
    # TODO: Delete user
    return "User %s" % username

if __name__ == "__main__":
    app.run(debug=True)
