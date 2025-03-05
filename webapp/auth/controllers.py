from .models import db
from flask import (Blueprint, redirect, request,
                   url_for, session, flash)
from .models import User
from oauthlib.oauth2 import WebApplicationClient
import requests
from config import DevConfig
import json
import os
from flask_login import current_user, LoginManager, login_user, logout_user, login_required

google_blueprint = Blueprint(
    'google', 
    __name__,
    url_prefix='/auth')

login_blueprint = Blueprint(
    'login',
    __name__,
    url_prefix='/reg-auth'
)

@login_blueprint.route('/login', methods=['GET', 'POST'])
def reg_login():
    if current_user.isauthenticated:
        flash("You're already logined")
        return redirect(url_for('main.index'))
    


os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
client_id = DevConfig.GOOGLE_CLIENT_ID
client_secret = DevConfig.GOOGLE_CLIENT_SECRET
client = WebApplicationClient(client_id)

authorization_url = 'https://accounts.google.com/o/oauth2/v2/auth'

token_url = 'https://oauth2.googleapis.com/token'

GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

@google_blueprint.route('/login')
def login():
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email"],
    )
    return redirect(request_uri)

@google_blueprint.route('/login/callback')
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]


    # Prepare and send request to get tokens! 
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code,
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(client_id, client_secret),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # We want to make sure their email is verified.
    # The user authenticated with Google, authorized our
    # app, and now we've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        #users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400
    
    user=User.query.filter_by(id=unique_id).first()
    if user is None:
        user = User(
            id=unique_id,
            #user_name=users_email, 
            email=users_email)
        db.session.add(user)
        db.session.commit()

    login_user(user)
    print(user)
        
    return redirect(url_for('web.mapView'))


@google_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))