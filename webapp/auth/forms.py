from flask_wtf import FlaskForm as Form
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, URL 
from .models import User 

class LoginForm(Form):
    username = StringField('Username', [DataRequired(), Length(max=225)])
    password = PasswordField('Password', [DataRequired()])
    remember = BooleanField('Remember Me')

    def validate(self):
        check_validate =  super(LoginForm, self).validate()
        if not check_validate:
            return False
        
        user=User.query.filter_by(email=self.email.data).first()
        if not user:
            self.email.errors.append('Invalid email or password')
            return False
        if not user.check_password(self.password.data):
            return False