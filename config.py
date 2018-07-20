import os.path
basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'storage.db')

SQLALCHEMY_TRACK_MODIFICATIONS = True

SECRET_KEY = 'hashsecurity'

UPLOAD_FOLDER = os.path.join(basedir, 'app/static/uploads/')
UPLOAD_FOLDER_PROFILE = os.path.join(basedir, 'app/static/uploads/profile/')
MAX_CONTENT_LENGTH = 16 * 1024 * 1024