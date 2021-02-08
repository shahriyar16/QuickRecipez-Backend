import gevent
from gevent import monkey
monkey.patch_all()
from requests.packages.urllib3.util.ssl_ import create_urllib3_context
create_urllib3_context()


from flask import Flask, jsonify, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from PIL import Image
import PIL
from AllRecipesScrape import *
from tfmodel import *
from recipe_search import *
from firebase_admin import credentials, firestore, initialize_app
import os
import logging






app = Flask(__name__)


# Initialize Firestore DB
cred = credentials.Certificate('key.json')
default_app = initialize_app(cred)
db = firestore.client()
todo_ref = db.collection('todos')

basedir = os.path.abspath(os.path.dirname(__file__))


# Initialize configs for the SQLite Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Instantiate the Database
db = SQLAlchemy(app)

# Create the Recipe class which will store all of the relevant information
class Recipe(db.Model):

    __tablename__ = 'Recipe Table'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.Text)
    ingredients = db.Column(db.String(200))

    def __init__(self, name, ingredients):
        self.name = name
        self.ingredients = ingredients

    def __repr__(self):
        return 'Recipe Name: {} Indredients: {}'.format(self.name, self.ingredients)

@app.route('/', methods = ['GET', 'POST'])
def hello():
    return 'Hello, this should be working!'



@app.route('/addpic', methods = ['GET', 'POST'])
def index():

    if request.method == "POST":
        app.logger.warning('testing warning log')
        req = request.files['image'].stream
        app.logger.error('testing error log')
        image = Image.open(req)
        app.logger.error('image has opened')
        save = image.save("testfood.jpg")
        app.logger.warning('image has opened')
        #print("Foods Detected: ", detect_foods(image))
        begin_search = find_recipe(detect_foods(image))
        app.logger.warning('searcher has started')
        return jsonify(begin_search)

        #image = Image.open(req)
        #print("Foods Detected: ", detect_foods(req))
        #begin_search = find_recipe(detect_foods(req))
        #return jsonify(begin_search)
        #f = request.form
        #for key in f.keys():
        #    for value in f.getlist(key):
        #        print(key,":",value)

    return 'Waiting for POST request'


port = int(os.environ.get('PORT', 8080))
if __name__ == "__main__":
    app.run(threaded=True, host='0.0.0.0', port=port)
