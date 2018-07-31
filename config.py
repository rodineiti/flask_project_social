import os.path
basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'storage.db')

SQLALCHEMY_TRACK_MODIFICATIONS = True

SECRET_KEY = 'hashsecurity'

UPLOAD_FOLDER = os.path.join(basedir, 'app/static/uploads/')
UPLOAD_FOLDER_PROFILE = os.path.join(basedir, 'app/static/uploads/profile/')
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

PUSHER_APP_ID = '567839'
PUSHER_KEY = '4574e10e7f8be933f7f5'
PUSHER_SECRET = '3bf0df1c2020dc43fbb8'
PUSHER_CLUSTER = 'us2'
PUSHER_SSL = True

MAIL_SERVER = 'mail.rdndeveloper.com'
MAIL_PORT = 465
MAIL_USERNAME = 'contact@rdndeveloper.com'
MAIL_PASSWORD = '4~bz=7~K}85o'
MAIL_USE_TLS = False
MAIL_USE_SSL = True