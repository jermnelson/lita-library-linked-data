__version_info__ = ('0', '0', '5')
__version__ = '.'.join(__version_info__)
__author__ = "Jeremy Nelson"
__license__ = 'GPL v2'
__copyright__ = '(c) 2013 by Jeremy Nelson'

import json
import os
from flask import Flask, g, redirect, render_template

URL_PREFIX = ''

app = Flask(__name__)

RESOURCES = {'articles_books': [],
             'software': [],
             'websites': []}

def load_resources(section, names):
    for name in names:
        RESOURCES[section].append(
            json.load(
                open(
                    os.path.join('static',
                                 'js',
                                 '{0}.json'.format(name)))))

load_resources('articles_books',
               ['linking-things-on-the-web',
                'understanding-marc-bibliographic'])

load_resources('websites',
               ['bibframe',
                'jinja',
                'rdfa-lite'])

@app.route('{0}/badge'.format(URL_PREFIX))
def badge():
    return render_template('badge.html')

@app.route('{0}/'.format(URL_PREFIX))
def home():
    return render_template('index.html')

@app.route('{0}/resources'.format(URL_PREFIX))
def resources():
    return render_template('resources.html',
                           resources=RESOURCES)

if __name__ == '__main__':
    host = '0.0.0.0'
    port = 8004

    app.run(host=host,
            port=port,
            debug=True)
