__version_info__ = ('0', '0', '5')
__version__ = '.'.join(__version_info__)
__author__ = "Jeremy Nelson"
__license__ = 'GPL v2'
__copyright__ = '(c) 2013 by Jeremy Nelson'

from flask import Flask, g, redirect, render_template

URL_PREFIX = ''

app = Flask(__name__)

@app.route('{0}/badge'.format(URL_PREFIX))
def badge():
    return render_template('badge.html')

@app.route('{0}/'.format(URL_PREFIX))
def home():
    return render_template('index.html')

@app.route('{0}/resources'.format(URL_PREFIX))
def resources():
    return render_template('resources.html')

if __name__ == '__main__':
    host = '0.0.0.0'
    port = 8004

    app.run(host=host,
            port=port,
            debug=True)
