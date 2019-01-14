from flask import Flask, jsonify, request, render_template
from models import Base, engine, Categories, Teams
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
from flask import make_response
from flask_httpauth import HTTPBasicAuth
import requests
import json

import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)
auth = HTTPBasicAuth()

engine = engine
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']


@app.route('/oauth/<provider>', methods=['POST'])
def login(provider):
    # STEP 1 - Parse the auth code
    auth_code = request.json.get('auth_code')
    print("Step 1 - Complete, received auth code %s" % auth_code)
    if provider == 'google':
        # STEP 2 - Exchange for a token
        try:
            # Upgrade the authorization code into a credentials object
            oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
            oauth_flow.redirect_uri = 'postmessage'
            credentials = oauth_flow.step2_exchange(auth_code)
        except FlowExchangeError:
            response = make_response(json.dumps('Failed to upgrade the authorization code.'), 401)
            response.headers['Content-Type'] = 'application/json'
            return response
        # Check that the access token is valid.
        access_token = credentials.access_token
        url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
        h = httplib2.Http()
        result = json.loads(h.request(url, 'GET')[1])
        # If there was an error in the access token info, abort.
        if result.get('error') is not None:
            response = make_response(json.dumps(result.get('error')), 500)
            response.headers['Content-Type'] = 'application/json'
        # Get user info
        h = httplib2.Http()
        userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
        params = {'access_token': credentials.access_token, 'alt': 'json'}
        answer = requests.get(userinfo_url, params=params)

        data = answer.json()

        name = data['name']
        picture = data['picture']
        email = data['email']

        # see if user exists, if it doesn't make a new one
        user = session.query(User).filter_by(email=email).first()
        if not user:
            user = User(username=name, picture=picture, email=email)
            session.add(user)
            session.commit()

        # STEP 4 - Make token
        token = user.generate_auth_token(600)

        # STEP 5 - Send back token to the client
        return jsonify({'token': token.decode('ascii')})

        # return jsonify({'token': token.decode('ascii'), 'duration': 600})
    else:
        return 'Unrecoginized Provider'


@app.route('/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii')})


@app.route('/')
@app.route('/home')
def show_catalog():
    categories = session.query(Categories).all()
    return render_template('catalog.html', categories=categories)


@app.route('/catalog/<category_id>/')
@app.route('/catalog/<category_id>/teams/')
def show_all_teams(category_id):
    category = session.query(Categories).filter_by(id=category_id).one()
    teams = session.query(Teams).filter_by(category_id=category.id).all()
    return render_template('listItems.html', category=category, teams=teams)


@app.route('/catalog/<category_id>/<team_id>/')
def show_team_detail(category_id, team_id):
    category = session.query(Categories).filter_by(id=category_id).one()
    team_deets = session.query(Teams).filter_by(category_id=category.id, id=team_id).one()
    return render_template('itemDeets.html', category=category_id, team_deets=team_deets)


@app.route('/catalog/<category_id>/<team_id>/edit', methods=['GET', 'POST'])
def edit_team(category_id, team_id):
    editedTeam = session.query(Teams).filter_by(id=team_id).one()
    if request.method == 'POST':
        if request.form['team_name']:
            editedTeam.name = request.form['team_name']
            session.add(editedTeam)
            session.commit()
            # flash('Team edited!')
            return redirect(url_for('show_all_teams', category_id=category_id))
    return render_template('editItem.html', category_id, team_id)


@app.route('/catalog/<category_id>/<team_id>/delete', methods=['GET', 'POST'])
def delete_team(category_id, team_id):
    teamToDelete = session.query(Teams).filter_by(id=team_id).one()
    if request.method == 'POST':
        if request.form['team_name']:
            teamToDelete.name = request.form['team_name']
            session.delete(teamToDelete)
            session.commit()
            # flash('Team edited!')
            return redirect(url_for('show_all_teams', category_id=category_id))
    return render_template('deleteItem.html', category_id, team_id)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
