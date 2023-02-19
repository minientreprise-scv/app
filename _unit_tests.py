import os
import subprocess
from configparser import ConfigParser
import pymongo.database
from planteqr import Database
from jinja2 import Environment

global error
error = False


def test_db():
    database = Database(config).get()
    assert type(database) == pymongo.database.Database


def test_templates():
    env = Environment()
    for template in os.listdir('templates/'):
        env.parse(open(f'templates/{template}').read())


def perform_unit_tests(tests):
    global error
    for test in tests:
        try:
            test[0]()
            print(f'\033[92m\t - {test[1]} ✔\033[0m')
        except:
            print(f'\t - \033[91mUnit test \'{test[1]}\' failed ❌\033[0m')
            error = True


def perform_test_run():
    global error
    try:
        subprocess.check_call(["python3", "serve.pyc"], timeout=15)
        print('\033[92mTest run ended successfully\033[0m')
    except subprocess.TimeoutExpired:
        print('\033[92mTest run ended successfully\033[0m')
    except Exception:
        error = True
        print('\033[91mTest run failed ❌\033[0m')


if __name__ == '__main__':
    config = ConfigParser()
    try:
        config.read('config.ini')
    except Exception:
        raise FileNotFoundError('Missing config.ini as described in README.md')
    print("\033[92mLoading configuration ✔\033[0m")

    print('\033[1mPerforming unit tests...\033[0m')

    perform_unit_tests([(test_db, 'Database'), (test_templates, 'Jinja Templates (HTML)')])

    print('\033[1mUnit tests ended successfully; now performing a test-run \033[0m')

    perform_test_run()

    if error:
        print('\n\n\033[1m\033[91mUnit tests finished with errors ❌\033[0m')
    else:
        print('\n\n\033[1m\033[92mAll tests have been passed !\033[0m')