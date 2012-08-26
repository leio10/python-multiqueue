from setuptools import setup    

setup(
    name='multiqueue',
    version='0.1.6',
    description='Sometimes when you use the Queue class in Python, you need to get an item from any of several queues. This small module implements an easy solution for this problem.',
    url='https://github.com/leio10/python-multiqueue',
    author='leio10',
    author_email='leiodd@gmail.com',
    install_requires=[],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=['multiqueue'],
    license='BSD',
    long_description="Sometimes when you use the Queue class in Python, you need to get an item from any of several queues.\n\
This small module implements an easy solution for this problem.\n\
\n\
MultiQueue class inherits from Queue and overrides internal methods of data access, \
sharing its interface but managing multiple queues instead of one.\n\
\n\
To add items to a MultiQueue, the put method must receive a tuple with the identifier of the queue as the first element and the value to be stored as the second element.\n\
\n\
When getting an item from a MultiQueue, you get a tuple indicating from which queue has been extracted and the extracted value.\n\
If there are items in multiple queues, these are obtained mixed, as applying the Round Robin algorithm.\n\
\n\
Furthermore, when instantiating the MultiQueue is possible to assign different weights to the queues, so that some have higher priority over others.\n\
If you have 2 queues in a MultiQueue, with weights 1 and 10 and both with a large number of elements, in 11 calls to get method you will obtain just one element from the first queue and 10 elements from the second."
)
