o from setuptools import setup
    
import os

root_dir = os.path.dirname(__file__)
if not root_dir:
    root_dir = '.'
long_desc = open(root_dir + '/README.md').read()

setup(
    name='multiqueue',
    version='0.1',
    description='Allows to wait for multiple queues with a single object. Employs weighted round-robin as scheduling algorithm.',
    url='https://github.com/leio10/python-multiqueue',
    author='Leio 10',
    author_email='leiodd@gmail.com',
    scripts=['multiqueue.py'],
    install_requires=[],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    license='BSD',
    long_description=long_desc,
)
