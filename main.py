import re
import secrets

from bson import ObjectId
from flask import Flask, render_template, make_response, redirect, request, send_file
from configparser import ConfigParser
from planteqr import Database, Plants, Documentation, Expenses

app = Flask('Une e-plante')
config = ConfigParser()
config.read('config.ini')
passphrases = config['administration']['passphrases'].split(',')
database = Database(config).get()
plants = Plants(database)
expenses = Expenses(database)


def has_registered_plant():
    if request.cookies.get('plants') is None:
        return False, []
    return True, request.cookies.get('plants').split(',')


def is_administrator():
    if request.cookies.get('admin') is None:
        return False
    if request.cookies.get('admin') in passphrases:
        return True
    return False


@app.route('/')
def accueil():
    return render_template('index.html')


@app.route('/admin/login', methods=['GET', 'POST'])
def log_administrator():
    if request.method == 'POST':
        form = request.form
        passphrase = form['passphrase']
        if passphrase in passphrases:
            response = make_response(redirect('/admin'))
            response.set_cookie('admin', passphrase)
        else:
            response = make_response(redirect('/admin/log'))
        return response
    return render_template('login.html')


@app.route('/admin')
def administration():
    if is_administrator():
        plants_sold_number = database.qr.count_documents({})
        plants_types_number = database.types.count_documents({})
        documentations_pages_number = database.documentation.count_documents({})
        plants_types = database.types.find({})
        documentations_pages = plants.get_documentation_by_flowers()
        documentation_types = Documentation.all_types()
        all_expense = expenses.get_expenses()
        balance_by_day = expenses.get_balance_ordered_by_days()
        balance_chart_labels = list(balance_by_day.keys())
        balance_chart_datas = [balance_by_day[day] for day in balance_chart_labels]
        return render_template('admin.html', sold=plants_sold_number, types=plants_types_number, documentations=documentations_pages_number, plants_types=list(plants_types), documentation_types=documentation_types, documentation_pages=documentations_pages, expenses=all_expense, expenses_chart=(balance_chart_labels, balance_chart_datas))
    return redirect('/admin/log')


@app.route('/admin/add-plant', methods=['POST'])
def add_plant():
    if is_administrator():
        form = request.form
        nom = form['name']
        description = form['description']
        photos = request.files.getlist('photos')
        slug = nom.lower().replace(' ', '-')
        images_paths = []
        for photo in photos:
            photo_id = secrets.token_urlsafe(16)
            ext = photo.filename.split('.')[-1]
            path = f'data/images/{slug}_{photo_id}.{ext}'
            photo.save(path)
            images_paths.append(path)
        plants.add_type(nom, description, images_paths, slug)
        return redirect('/admin')
    return redirect('/admin/log')


@app.route('/admin/add-expense', methods=['POST'])
def add_expense():
    if is_administrator():
        form = request.form
        value = form['value']
        comment = form['comment']
        expenses.add(float(value), comment)
        return redirect('/admin')
    return redirect('/admin/log')


@app.route('/admin/add-documentation', methods=['POST'])
def add_documentation():
    if is_administrator():
        form = request.form
        title = form['title']
        step = form['step']
        content = form['content']
        sections = content.split('%section%')
        sections[-1] = sections[-1].split('%suite%')[0]
        next_step_requirements = re.search('%suite%([\s\S]*?)%suite-fin%', content).group().replace('%suite%', '').replace('%suite-fin%', '')
        if request.args.get('update') is None:
            plant = form['plant']
            plants.add_documentation(ObjectId(plant), Documentation(step), title, next_step_requirements, sections)
        elif request.args.get('doc') is not None:
            documentation = ObjectId(request.args.get('doc'))
            plants.update_documentation(documentation, Documentation(step), title, next_step_requirements, sections)
        return redirect('/admin')
    return redirect('/admin/log')


@app.route('/admin/generate-qr')
def generate_qr():
    if is_administrator():
        plant = request.args.get('plant')
        if plant is None:
            return {'message': 'Veuillez indiquer une plante'}
        sold_plant = plants.generate_qr(ObjectId(plant))
        return send_file(f'data/qr/{sold_plant.id}.png'), 200
    return redirect('/admin/log')


@app.route('/@<sale_id>')
def add_plant_to_navigator(sale_id):
    plant = plants.get_plant(sale_id)
    if plant.data is None:
        return redirect('/')
    has_plants, registered_plants = has_registered_plant()
    if has_plants and sale_id not in registered_plants or not has_plants:
        registered_plants.append(sale_id)
        response = make_response(redirect('/dashboard'))
        response.set_cookie('plants', ','.join(registered_plants))
        return response
    return redirect('/')


@app.route('/data/<media_type>/<file>')
def deliver_media(media_type, file):
    return send_file(f'data/{media_type}/{file}')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
