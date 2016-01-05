from setuptools import setup, find_packages

setup(
    name = 'ithkuil',
    version = '0.1',
    packages = find_packages(),
    
    description = 'A Python module implementing utilities for the Ithkuil constructed language',
    
    url = 'https://github.com/fizyk20/ithkuil',
    
    author = 'Bartłomiej Kamiński',
    author_email = 'fizyk20@gmail.com',
    
    license = 'GPLv3',
    
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ],
    
    keywords = 'ithkuil',
    
    install_requires = ['sqlalchemy'],
    
    package_data = {
        '': ['*.db']
    }
)