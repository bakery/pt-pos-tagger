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

app.config['PARSE_APPLICATION_ID'] = os.environ.get('PARSE_APPLICATION_ID', '3qytb5EL7BSVhLYhqL7j47cc7nThzRxUknuSGMv5')
app.config['PARSE_API_KEY'] = os.environ.get('PARSE_API_KEY', 'e00zv4zpr81fBPC5N05LO6c8vCwBjVLzZCLXOD7G')

tagger_options = {
    'parse_app_id': '3qytb5EL7BSVhLYhqL7j47cc7nThzRxUknuSGMv5', #app.config['PARSE_APPLICATION_ID'],
    'parse_api_key': 'e00zv4zpr81fBPC5N05LO6c8vCwBjVLzZCLXOD7G', #app.config['PARSE_API_KEY'],
    'tagger_filename': './static/models/tagger.pickle',
    'sentence_tokenizer_filename': './static/models/punkt/portuguese.pickle'
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
