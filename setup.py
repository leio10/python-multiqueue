from setuptools import setup    

setup(
    name='multiqueue',
    version='0.1.2',
    description='Allows to wait for multiple queues with a single object. Employs weighted round-robin as scheduling algorithm. Queues are identified by ids, that are used on Put and Get operations.',
    url='https://github.com/leio10/python-multiqueue',
    author='Leio 10',
    author_email='leiodd@gmail.com',
    install_requires=[],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    license='BSD',
)
