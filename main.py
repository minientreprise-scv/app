import datetime
import random
import re
import secrets

import markdown
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


@app.route('/scan')
def scan():
    return render_template('scan.html')


@app.route('/dashboard')
def dashboard():
    has_plants, registered_plants_ids = has_registered_plant()
    if has_plants:
        registered_plants = [plants.get_plant(_id).data for _id in registered_plants_ids]
        if request.args.get('plant') is None:
            selected = registered_plants[0]
        else:
            selected = plants.get_plant(request.args.get('plant')).data
            if selected is None:
                selected = registered_plants[0]
        documentations = plants.get_documentation_by_flowers()[str(selected['plant'])]
        return render_template('dashboard.html', plants=registered_plants, selected=selected, documentations=documentations)
    return redirect('/scan')


@app.route('/dashboard/add-image', methods=['POST'])
def add_image():
    form = request.form
    plant = form.get('plant')
    if plant is not None:
        image = request.files.get('photo')
        image_id = secrets.token_urlsafe(16)
        image_ext = image.filename.split('.')[-1]
        image_filename = f'{image_id}.{image_ext}'
        image_path = f'data/images/{image_filename}'
        image.save(image_path)
        plants.get_plant(plant).add_image(datetime.datetime.now(), image_path)
        return redirect(f"/dashboard?plant={plant}")
    return redirect('/dashboard')


@app.route('/dashboard/change-name', methods=['POST'])
def change_name():
    form = request.form
    if form.get('plant') is not None:
        plants.get_plant(form.get('plant')).change_name(form.get('name'))
        return redirect(f"/dashboard?plant={form.get('plant')}")
    return redirect('/dashboard')


@app.route('/admin/login', methods=['GET', 'POST'])
def log_administrator():
    if request.method == 'POST':
        form = request.form
        passphrase = form['passphrase']
        if passphrase in passphrases:
            response = make_response(redirect('/admin'))
            response.set_cookie('admin', passphrase)
        else:
            response = make_response(redirect('/admin/login'))
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
    return redirect('/admin/login')


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
    return redirect('/admin/login')


@app.route('/admin/add-expense', methods=['POST'])
def add_expense():
    if is_administrator():
        form = request.form
        value = form['value']
        comment = form['comment']
        expenses.add(float(value), comment)
        return redirect('/admin')
    return redirect('/admin/login')


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
    return redirect('/admin/login')


@app.route('/admin/generate-qr')
def generate_qr():
    if is_administrator():
        plant = request.args.get('plant')
        if plant is None:
            return {'message': 'Veuillez indiquer une plante'}
        sold_plant = plants.generate_qr(ObjectId(plant))
        return send_file(f'data/qr/{sold_plant.id}.png'), 200
    return redirect('/admin/login')


@app.route('/@<sale_id>')
def add_plant_to_navigator(sale_id):
    plant = plants.get_plant(sale_id)
    if plant.data is None:
        return 'Aucune plante trouvée... <a href="/scan">Réessayer</a> ou <a href="mailto:armand@camponovo.xyz">nous contacter</a>'
    has_plants, registered_plants = has_registered_plant()
    if has_plants and sale_id not in registered_plants:
        registered_plants.append(sale_id)
        response = make_response(redirect('/dashboard'))
        response.set_cookie('plants', ','.join(registered_plants), max_age=60 * 60 * 24 * 365 * 2)
        return response
    elif sale_id in registered_plants:
        return redirect('/dashboard')
    elif not has_plants:
        response = make_response(redirect('/dashboard'))
        response.set_cookie('plants', sale_id, max_age=60 * 60 * 24 * 365 * 2)
        return response
    return redirect('/')


@app.route('/data/<media_type>/<file>')
def deliver_media(media_type, file):
    return send_file(f'data/{media_type}/{file}')


def get_icon_by_state(state):
    return {'planter': ('fa-hand-holding-seedling', 'is-info'), 'pousser': ('fa-leaf', 'is-success'), 'rempoter': ('fa-shovel', 'is-brown'), 'autre': (random.choice(['fa-wheat', 'fa-rainbow', 'fa-flower', 'fa-flower-tulip', 'fa-flower-daffodil']), 'is-link')}[state]


def md_to_html(markdown_content):
    return markdown.markdown(markdown_content)


if __name__ == '__main__':
    app.jinja_env.globals.update(get_icon_by_state=get_icon_by_state)
    app.jinja_env.globals.update(md_to_html=md_to_html)
    app.run(host='0.0.0.0', port=8080, debug=True)
