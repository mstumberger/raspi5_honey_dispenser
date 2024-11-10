import pathlib
import pkg_resources
from setuptools import setup, find_packages

# https://stackoverflow.com/a/59971469/9676376
with pathlib.Path('requirements.txt').open() as requirements_txt:
    install_requires = [
        str(requirement)
        for requirement
        in pkg_resources.parse_requirements(requirements_txt)
    ]

from setuptools import setup

setup(
    name='HoneyDispenser',
    version='0.1',
    packages=[
        'mstumb',
        'mstumb.honey_dispenser',
        'mstumb.honey_dispenser.gui',
        'mstumb.honey_dispenser.gui.gauge',
        'mstumb.honey_dispenser.gui.frames',
        'mstumb.honey_dispenser.gpio',
        'mstumb.honey_dispenser.config',
        'mstumb.honey_dispenser.scaling'
    ],
    package_dir={'': 'src'},
    url='',
    license='',
    author='pi',
    author_email='',
    description='',
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'dispenser = mstumb.__main__:main',  # This calls the __main__.py file
        ],
    },
)
