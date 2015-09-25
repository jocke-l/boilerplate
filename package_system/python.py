import re
import string
from os import path, makedirs
from unicodedata import normalize
from jinja2 import Environment, PackageLoader

TEMPLATE_PATH = path.join('templates', 'python')

env = Environment(loader=PackageLoader(__package__, TEMPLATE_PATH))


def to_ascii(s):
    return ''.join(c for c in s if c in string.printable)


def friendly(string):
    parts = re.sub(
        '[^ \w]', '', normalize('NFC', string).replace('-', ' ')
    ).lower().split()

    user_friendly = to_ascii('-'.join(parts))
    python_friendly = to_ascii('_'.join(parts))

    return user_friendly, python_friendly


def make_package_dir(destination_path, version, name):
    package_name_user, package_name_python = friendly(name)

    package_root = path.join(destination_path,
                             '{}-{}'.format(package_name_user, version))
    package_dir = path.join(package_root, package_name_python)

    try:
        makedirs(package_dir)
    except OSError:
        pass

    return package_root, package_dir


def create_package(destination_path, setup_params, source):
    setup_template = env.get_template('setup.py')
    setup_script = setup_template.render(setup_params)

    package_root, package_dir = make_package_dir(destination_path,
                                                 setup_params['version'],
                                                 setup_params['name'])

    with open(path.join(package_root, 'setup.py'), 'w') as setup_file:
        setup_file.write(setup_script)

    with open(path.join(package_dir, '__init__.py'), 'w') as source_file:
        source_file.write(source)
