from flask import Flask
from configparser import ConfigParser
import pymongo
from planteqr import Database

app = Flask('Une e-plante')
config = ConfigParser()
config.read('config.ini')
database = Database(config).get()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
