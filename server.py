"""
Module for LITA Linked Data Webinar

Copyright (C) 2014 Jeremy Nelson

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""
__version_info__ = ('0', '1', '0')
__version__ = '.'.join(__version_info__)
__author__ = "Jeremy Nelson"
__license__ = 'GPL v2'
__copyright__ = '(c) 2013, 2014 by Jeremy Nelson'

import datetime
import json
import os
import sys
import uuid
from flask import Flask, g, jsonify, redirect, render_template
from flask import abort, url_for

URL_PREFIX = '/lita-webinar-2014'

app = Flask(__name__)

RESOURCES = {'articles_books': [],
             'software': [],
             'websites': []}

IDENTITY_SALT = 'lita-experiments-marc-linked-data'

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
                'dublin-core',
                'marc',
                'marc-bibliographic',
                'mods',
                'rdfa-lite',
                'schema-bib-extend-community-group',
                'schema-org'])

@app.route('{0}/coding-marc-linked-data-<metal>-badge.json'.format(URL_PREFIX))
def badge_class(metal):
    if not metal in ['bronze', 'silver', 'gold']:
        abort(404)
    return jsonify({
        "name": "Coding Experiments with MARC and Linked Data {0} Badge".format(
        metal.title()),
        "description": """This {0} badge is for the LITA Linked Data Webinar Series -
Coding Experiments with MARC and Linked Data by Jeremy Nelson on 14 January
2014.""".format(metal),
        "image": "http://intro2libys.info{0}".format(
            url_for('static', filename="{0}-badge-template.png".format(metal))),
        "criteria": "http://intro2libys.info{0}".format(
            url_for('badge')),
        "tags": ["LITA", "Libraries", "Linked Data", "MARC"],
        "issuer": "http://intro2libsy.info{0}".format(
            url_for('badge_issuer_org'))})

@app.route('{0}/badge-issuer-organization.json'.format(URL_PREFIX))
def badge_issuer_org():
    return jsonify(
        {"name": "intro2libsys.info LLC",
         "url": "http://intro2libsys.info",
         "email": "jermnelson@gmail.com",
         "revocationList": "http://intro2libsys.info{0}".format(
             url_for('badge_revoked'))})

@app.route('{0}/revoked.json'.format(URL_PREFIX))
def badge_revoked():
    return jsonify({})

@app.route("{0}/<uid>-coding-marc-linked-data-badge.json".format(URL_PREFIX))
def badge_for_participant(uid):
    participant_badge_location = os.path.join('badges', '{0}.json'.format(uid))
    if os.path.exists(participant_badge_location):
        participant_badge = json.load(open(badge_for_participant, 'rb'))
        return jsonfiy(participant_badge)
    else:
        abort(404)

@app.route("{0}/<uid>-coding-marc-linked-data-badge.png".format(URL_PREFIX))
def badge_image_for_participant(uid):
    participant_img_location = os.path.join('badges',
                                            'img',
                                            '{0}.png'.format(uid))
    if os.path.exists(participant_img_location):
        img = None
        with open(participant_img_location, 'rb') as img_file:
            img = img_file.read()
        return Request(img, mimetype='image/png')
    else:
        abort(404)

def bake_badge(**kwargs):
    assert_url = kwargs.get('url')
    try:
        baking_service = urllib2.urlopen(
            'http://beta.openbadges.org/baker?assertion={0}'.format(assert_url))
        raw_image = baking_service.read()
        return raw_image
    except:
        print("Exception occurred: {0}".format(sys.exc_info()[0]))
        return None

def issue_badge(**kwargs):
    identity_hash = hashlib.sha256(kwargs.get("email"))
    identity_hash.update(IDENTITY_SALT)
    uid = str(uuid.uuid4()).split("-")[0]
    badge_json = {
        'badge': "http://intro2libys.info{0}".format(
            url_for('badge_class', metal=kwargs.get('metal'))),
        'issuedOn': kwargs.get('issuedOne', datetime.now().isoformat()),
        'recipient': {
            'type': kwargs.get("email"),
            'hashed': True,
            'salt': IDENTITY_SALT,
            'identity': "sha256${0}".format(
                identity_hash.hexdigest())},
        'verify': {
            'type': 'hosted',
            'url': "http://intro2libsys.info{0}/"\
            "{1}-coding-marc-linked-data-badge.json".format(
                URL_PREFIX,
                uid)},
        'uid': uid
        }
    # Save badge to badges directory
    json.dump(badge_json,
              open(os.path.join('badges', '{0}.json'.format(uid)), 'wb'),
              indent=2,
              sort_keys=True)
    raw_badge_img = bake_badge(url=url_for('badge_for_participant',
                                           uid=uid))
    if raw_badge_img:
        with open(os.path.join('badges', 'img', '{0}.png'.format(uid)), 'wb') as img_file:
            img_file.write(raw_badge_img)
        print("Successfully added {0} and badge image".format(uid))
    else:
        print("ERROR unable to issue badge")

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
