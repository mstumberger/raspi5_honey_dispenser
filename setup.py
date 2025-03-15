import pathlib
import pkg_resources

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
        'mstumb.honey_dispenser.gui.top_level',
        'mstumb.honey_dispenser.gpio',
        'mstumb.honey_dispenser.config',
        'mstumb.honey_dispenser.scaling'
    ],
    package_dir={'': 'src'},
    url='https://github.com/mstumberger/raspi5_honey_dispenser',
    author='Marko Štumberger',
    author_email='marko.stumberger@gmail.com',
    description=f'Raspberry PI 5 honey dispenser with '
                f'HX711 and 5kg load cell and ULN2003 stepper motor driver and 28BYJ Stepper Motor',
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'dispenser = mstumb.__main__:main',  # This calls the main function in __main__.py file
        ],
    },
)
