#!/home/jpnelson/jpn-app-dev/bin/python

from flup.server.fcgi import WSGIServer
from server import app

if __name__ == '__main__':
    WSGIServer(app,
               bindAddress=('0.0.0.0', 8004)).run()
