from flask import Flask, render_template
from configparser import ConfigParser
from planteqr import Database

app = Flask('Une e-plante')
config = ConfigParser()
config.read('config.ini')
database = Database(config).get()


@app.route('/')
def accueil():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
