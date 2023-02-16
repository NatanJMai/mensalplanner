import configparser
import pandas as pd
import database.db_functions as db
from flask_mysqldb import MySQL

def config_to_flask(app, config):
    app.config['MYSQL_HOST'] = config['mysql']['host']
    app.config['MYSQL_USER'] = config['mysql']['user']
    app.config['MYSQL_PASSWORD'] = config['mysql']['passwd']
    app.config['MYSQL_DB']       = config['mysql']['db']
    return app

def run(app):
    config = db.reading_from_file()
    app    = config_to_flask(app, config)

    return app


