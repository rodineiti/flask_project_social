import os.path
basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'storage.db')

SQLALCHEMY_TRACK_MODIFICATIONS = True

SECRET_KEY = ''

UPLOAD_FOLDER = os.path.join(basedir, 'app/static/uploads/')
UPLOAD_FOLDER_PROFILE = os.path.join(basedir, 'app/static/uploads/profile/')
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

PUSHER_APP_ID = ''
PUSHER_KEY = ''
PUSHER_SECRET = ''
PUSHER_CLUSTER = ''
PUSHER_SSL = True

MAIL_SERVER = ''
MAIL_PORT = 465
MAIL_USERNAME = ''
MAIL_PASSWORD = ''
MAIL_USE_TLS = False
MAIL_USE_SSL = True