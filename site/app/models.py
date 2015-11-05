from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    pwd = db.Column(db.String(64)) # TODO: Encyrption
    email = db.Column(db.String(120), unique=True)
    imgur_user = db.relationship('Imgur_User', backref='user') #TODO: true 1-to-1 relationship

    def __repr__(self):
        return '<User %r>' % (self.username)

class Imgur_User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # 255 varchar size for tokens
    access_token = db.Column(db.String(255)) 
    refresh_token = db.Column(db.String(255))
    last_refresh = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __repr__(self):
        return '<Imgur_User %r>' % (self.access_token)
