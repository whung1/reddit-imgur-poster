from app import db
import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    pwd = db.Column(db.String())
    email = db.Column(db.String(120))
    authenticated = db.Column(db.Boolean, default=False)
    imgur_user = db.relationship('Imgur_User', uselist=False, backref='user')
    reddit_user = db.relationship('Reddit_User', uselist=False, backref='user')

    def is_active(self):
        """All users are active by default"""
        return True
    
    def get_id(self):
        """Return the id in UNICODE to 
        satisfy Flask-Login's requirements."""
        return unicode(self.id)

    def is_authenticated(self):
        """Return True if the user 
        is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False
    
    def __repr__(self):
        return '<User %r>' % (self.username)

class Imgur_User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    # 255 varchar size for tokens
    access_token = db.Column(db.String(255)) 
    refresh_token = db.Column(db.String(255))
    last_refresh = db.Column(db.DateTime, 
            default = datetime.datetime.now,
            onupdate = datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __repr__(self):
        return '<Imgur_User %r>' % (self.username)

class Reddit_User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    # 255 varchar size for tokens
    access_token = db.Column(db.String(255)) 
    refresh_token = db.Column(db.String(255))
    #last_refresh = db.Column(db.DateTime, 
    #        default = datetime.datetime.now,
    #        onupdate = datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __repr__(self):
        return '<Imgur_User %r>' % (self.username)
