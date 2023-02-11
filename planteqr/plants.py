import datetime
import secrets

from PIL import Image
from qrcode import QRCode, ERROR_CORRECT_H
import pymongo.database
from bson import ObjectId
from flask import request


class Documentation:
    plant = 'plant'
    grow = 'grow'
    repot = 'repot'

    def __init__(self, type):
        self.type = type

    def __str__(self):
        return self.type


def saveQr(data, filename):
    logo = Image.open(f'static/assets/charte/qr.png')
    basewidth = 115
    wpercent = (basewidth / float(logo.size[0]))
    hsize = int((float(logo.size[1]) * float(wpercent)))
    logo = logo.resize((basewidth, hsize))
    qr = QRCode(error_correction=ERROR_CORRECT_H)
    qr.add_data(data)
    qr.make()
    qrimg = qr.make_image(fill_color="#252525", back_color="#e0e0e0").convert('RGBA')
    pos = ((qrimg.size[0] - logo.size[0]) // 2, (qrimg.size[1] - logo.size[1]) // 2)
    qrimg.paste(logo, pos)
    qrimg.save(f'data/qr/{filename}')


class Plants:

    def __init__(self, database: pymongo.database.Database):
        self.db = database

    def add_type(self, name: str, description: str, images: list):
        slug = name.lower().replace(' ', '-')
        self.db.types.insert_one(
            {
                'name': name,
                'description': description,
                'images': images,
                'slug': slug
            }
        )

    def add_documentation(self, plant_type_id: ObjectId, documentation_type: Documentation, title: str, next_step_requirements: list):
        self.db.documentation.insert_one(
            {
                'plant': plant_type_id,
                'state': str(documentation_type),
                'title': title,
                'next_step_requirements': next_step_requirements
            }
        )

    def get_all_types(self):
        return self.db.types.find()

    def get_plant(self, sale_id):
        return SoldPlant(self.db, sale_id)

    def generate_qr(self, plant_type_id: ObjectId):
        qr_id = secrets.token_urlsafe(16)
        hostname = request.host_url
        saveQr(f'{hostname}/@{qr_id}', f'{qr_id}.png')
        self.db.qr.insert_one(
            {
                'plant': plant_type_id,
                'image': f'{qr_id}.png',
                'sale_id': qr_id,
                'images': []
            }
        )

        return SoldPlant(self.db, qr_id)


class SoldPlant:

    def __init__(self, database: pymongo.database.Database, sale_id: str):
        self.db = database
        self.id = sale_id
        self.data: pymongo.cursor.Cursor
        self._update_data()

    def _update_data(self):
        self.data = self.db.qr.find_one({'sale_id': self.id})

    def add_image(self, date: datetime.datetime, image: str):
        images = self.data['images']
        images.append({
            'path': image,
            'date': date
        })
        self.db.update_one({'sale_id': self.data['sale_id']}, {'$set': {'images': images}})