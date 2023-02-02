from flask import Flask

app = Flask('Une e-plante')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
