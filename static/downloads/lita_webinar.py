"""
 :module:`lita_webinar`

 This module launches a simple Flask application for use by
 students in the January 14th 2014 LITA webinar, *Coding
 experiments with MARC and Linked Data* at
 <http://intro2libsys.info/lita-linked-data-webinar-2014>

"""
__version_info__ = ('1', '0', '0')
__version__ = '.'.join(__version_info__)
__author__ = "Jeremy Nelson"
__license__ = 'GPL v2'
__copyright__ = '(c) 2013 by Jeremy Nelson'

import json
import os
from flask import Flask, g, redirect, render_template

app = Flask(__name__)

@app.route('/')
def index():
    "Default view for Flask Web App"
    if os.path.exists(os.path.join('templates',
                                    'index.html')):
        return render_template('index.html')
    else:
        return """Index.html template does not exists"""

if __name__ == '__main__':
    host = '0.0.0.0'
    port = 8080

    app.run(host=host,
            port=port,
            debug=True)