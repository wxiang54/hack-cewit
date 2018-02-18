from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
import json
import config
#from raven.contrib.flask import Sentry

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
toolbar = DebugToolbarExtension(app)
#sentry = Sentry(app, dsn='https://705f20eced1b46aab4114160bf82fe75:a941826f6ab14af3ac15a8ef75d6f86b@sentry.i\o/270395')                                                                                                    

from views import *

if __name__ == "__main__":
    app.run()

