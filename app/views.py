from flask import Flask, jsonify, request, render_template, g, flash
from models import Base, engine, Categories, Teams, User
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
from flask import make_response
from flask_httpauth import HTTPBasicAuth
import requests
import json
import random
import string
from flask import session as login_session

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


@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('clientOAuth.html', STATE=state)


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token

    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.8/me"
    '''
        Due to the formatting for the result from the server token exchange we have to
        split the token first on commas and select the first index which gives us the key : value
        for the server access token then we split it on colons to pull out the actual token value
        and replace the remaining quotes with nothing so that it can be used directly in the graph
        api calls
    '''
    token = result.split(',')[0].split(':')[1].replace('"', '')

    url = 'https://graph.facebook.com/v2.8/me?access_token=%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout
    login_session['access_token'] = token

    # Get user picture
    url = 'https://graph.facebook.com/v2.8/me/picture?access_token=%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '

    flash("Now logged in as %s" % login_session['username'])
    return output


@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id, access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"


# User Helper Functions


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


@app.route('/')
@app.route('/home')
def show_catalog():
    categories = session.query(Categories).all()
    if 'username' not in login_session:
        return render_template('publicCatalog.html', categories=categories)
    else:
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
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
