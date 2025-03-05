import os

def create_module(app, **kwargs):
    secret=os.urandom(12)
    app.secret_key = secret
    from .controllers import app_blueprint
    app.register_blueprint(app_blueprint)