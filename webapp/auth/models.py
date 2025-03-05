
from .. import db
from . import AnonymousUserMixin
from wtforms import PasswordField, StringField
from wtforms.validators import InputRequired, EqualTo
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm

class User(db.Model):
    id = db.Column(db.String(8), primary_key=True)
    email = db.Column(db.String(255))
    user_name = db.Column(db.String(255))
    pwdhash = db.Column(db.String())

    def __init__(self, email, id, password, username):
        self.id = id
        self.email = email
        self.user_name = username
        self.pwdhash = generate_password_hash(password)

    def __repr__(self):
        return '<User {}>'.format(self.user_name)

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)
    
    @property
    def is_authenticated(self):
        if isinstance(self, AnonymousUserMixin):
            return False
        else:
            return True 
        
    def get_id(self):
        return str(self.id)
    
    def is_active(self):
        # Replace this condition with your own logic to determine if the user is active
        return True
    
class LoginForm(FlaskForm):
    username = StringField('Username', [InputRequired()])
    password = PasswordField('Password',[InputRequired()])