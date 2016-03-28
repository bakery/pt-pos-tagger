# -*- coding: utf-8 -*-

"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/

This file creates your application.
"""

import os
import sys
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template, request, redirect, url_for
from flask_restful import Resource, Api, reqparse
from tagger import Tagger

app = Flask(__name__)
api = Api(app)

CONFIG_KEYS = ['PARSE_APP_ID','PARSE_API_KEY','TAGGER_FILENAME','SENTENCE_TOKENIZER_FILENAME']
for k in CONFIG_KEYS:
    app.config[k] = os.environ.get(k)

tagger_options = {
    'parse_app_id': app.config['PARSE_APP_ID'],
    'parse_api_key': app.config['PARSE_API_KEY'],
    'tagger_filename': app.config['TAGGER_FILENAME'],
    'sentence_tokenizer_filename': app.config['SENTENCE_TOKENIZER_FILENAME']
}
tagger = Tagger(tagger_options)

parser = reqparse.RequestParser()
parser.add_argument('text')

class TaggerResource(Resource):
     def post(self):        
        args = parser.parse_args()
        return {
            'sentences': tagger.tag_text(args['text'])
        }

api.add_resource(TaggerResource, '/tagger')


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')


###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    handler = RotatingFileHandler('./app.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run(debug=True)
