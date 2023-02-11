from bson import ObjectId
from flask import Flask, render_template, make_response, redirect, request
from configparser import ConfigParser
from planteqr import Database, Plants

app = Flask('Une e-plante')
config = ConfigParser()
config.read('config.ini')
database = Database(config).get()
plants = Plants(database)


def has_registered_plant():
    if request.cookies.get('plants') is None:
        return False, []
    return True, request.cookies.get('plants').split(',')


@app.route('/')
def accueil():
    return render_template('index.html')


@app.route('/@<sale_id>')
def add_plant_to_navigator(sale_id):
    plant = plants.get_plant(sale_id)
    if plant.data is None:
        return redirect('/')
    has_plants, registered_plants = has_registered_plant()
    if has_plants and sale_id not in registered_plants:
        registered_plants.append(sale_id)
        response = make_response(redirect('/dashboard'))
        response.set_cookie('plants', ','.join(registered_plants))
        return response
    return redirect('/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
