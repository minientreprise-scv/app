import datetime
import locale

import pymongo.database
import pytz

timezone = pytz.timezone('Europe/Paris')
locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')


class Expenses:

    def __init__(self, database: pymongo.database.Database):
        self.db = database

    def add(self, value: float, comment: str):
        date = datetime.datetime.now(tz=timezone)
        readable_date = date.strftime('%d %b %Y à %H:%M')
        self.db.expenses.insert_one(
            {
                'date': date,
                'readable_date': readable_date,
                'value': value,
                'comment': comment
            }
        )

    def get_expenses(self):
        return self.db.expenses.find({})

    def get_balance_ordered_by_days(self):
        expenses = self.db.expenses.find({}).sort([('$natural', -1)])
        balance = 0
        balance_by_day = {}
        for expense in expenses:
            balance = balance + expense['value']
            date_key = expense['readable_date'].split(' 20')[0]
            balance_by_day[date_key] = balance
        return balance_by_day
