from flask import Flask, jsonify, request, render_template
from models import Base, engine, Categories, Teams
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

engine = engine
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)


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
