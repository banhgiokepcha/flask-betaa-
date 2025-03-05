from flask import ( session, abort, flash)
from flask_login import LoginManager, login_fresh, login_user, current_user, AnonymousUserMixin
import os
from .controllers import google_blueprint, login_blueprint


class WebAnonymous(AnonymousUserMixin):
    def __init__(self):
        self.username = 'Anon'

login_manager = LoginManager()
login_manager.anonymous_user = WebAnonymous



def create_module(app, **kwargs):
    secrets = os.urandom(24)
    app.secret_key = secrets
    login_manager.init_app(app)
    app.register_blueprint(google_blueprint)
    app.register_blueprint(login_blueprint)
     
    
@login_manager.user_loader
def load_user(userId):
    from .models import User 
    return User.query.get(userId) 



        


    
    
