from flask import Flask

WTF_CSRF_ENABLED = False
WTF_CSRF_SECRET_KEY = 'wowlad'

UPLOAD_DIR = 'uploads'

# config - aside from our database, the rest is for use by Flask
DEBUG = True
DATABASE = True
TEMPLATE_FOLDER = '../templates/'

# create a flask application - this ``app`` object will be used to handle
# inbound requests, routing them to the proper 'view' functions, etc
app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config.from_object(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!1l3k1;l23kl1;2k3l;12kRT'

import obi.views
import obi.db