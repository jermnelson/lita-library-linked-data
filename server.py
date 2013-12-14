__version_info__ = ('0', '0', '5')
__version__ = '.'.join(__version_info__)
__author__ = "Jeremy Nelson"
__license__ = 'GPL v2'
__copyright__ = '(c) 2013 by Jeremy Nelson'

import json
import os
from flask import Flask, g, jsonify, redirect, render_template

URL_PREFIX = ''

app = Flask(__name__)

RESOURCES = {'articles_books': [],
             'software': [],
             'websites': []}

def load_resources(section, names):
    """
    Function loads JSON resources based on a section and a list of json file
    names.

    :param section: Section in RESOURCES dict, should be restricted to 3 values
    :param names: List of json filename
    """
    for name in names:
        RESOURCES[section].append(
            json.load(
                open(
                    os.path.join('static',
                                 'js',
                                 '{0}.json'.format(name)))))

load_resources('articles_books',
               ['expressing-dublin-core-metadata',
                'linking-things-on-the-web',
                'understanding-marc-bibliographic'])

load_resources('software',
               ['bootstrap',
                'jinja',
                'jquery',
                'knockout-js',
                'pymarc',
                'python-programming-language',
                'rdflib',
                'reveal-js'])

load_resources('websites',
               ['bibframe',
                'rdfa-lite',
                'schema-org'])

@app.route('{0}/badge'.format(URL_PREFIX))
def badge():
    return render_template('badge.html')

@app.route('{0}/downloads'.format(URL_PREFIX))
def downloads():
    return render_template('downloads.html')

@app.route('{0}/'.format(URL_PREFIX))
def home():
    return render_template('index.html')

@app.route('{0}/resources'.format(URL_PREFIX))
def resources():
    return render_template('resources.html',
                           resources=RESOURCES)

@app.route('{0}/resources/<filename>.json'.format(URL_PREFIX))
def resource_json(filename=None):
    for section in RESOURCES.keys():
        for json_info in RESOURCES[section]:
            if filename == json_info.get('name'):
                return jsonify(json_info)
    return jsonify({'error': '{0}.json not found'.format(filename)})

if __name__ == '__main__':
    host = '0.0.0.0'
    port = 8004

    app.run(host=host,
            port=port,
            debug=True)
