from flask import Flask, jsonify, request, render_template
from models import Base, engine, Categories, Items
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
    return render_template('catalog.html')


@app.route('/catalog/<category>/items/')
def show_all_items(category):
    return render_template('listItems.html')


@app.route('/catalog/<category>/<item>/')
def show_item_detail(category, item):
    return render_template('itemDeets.html')


@app.route('/catalog/<category>/<item>/edit')
def edit_item(category, item):
    return render_template('editItem.html')


@app.route('/catalog/<category>/<item>/delete')
def delete_item(category, item):
    return render_template('deleteItem.html')


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
