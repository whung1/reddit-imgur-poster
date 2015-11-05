import os
basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = 'Sm9obiBTY2hyb20ga2lja3MgYXNz'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
