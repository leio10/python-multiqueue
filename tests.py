#!/usr/bin/env python

"""
    multiqueue.tests
~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2012 by Leonardo Diez.
:license: BSD, see LICENSE for more details.
"""

from multiqueue import MultiQueue, InvalidQueue
import Queue, time
import unittest

class TestMultiQueue(unittest.TestCase):

    def setUp(self):
        pass

    def test_normal(self):
        q = MultiQueue()
        q.put((1,2))
        self.assertEqual(q.get(),(1,2))
        q.put((2,4))
        self.assertEqual(q.get(),(2,4))
        q.put((1,1))
        self.assertEqual(q.get(),(1,1))
    
    def test_noresize(self):
        q = MultiQueue(num_queues=5)
        self.assertRaises(InvalidQueue, q.put, (6, 1))
        
    def test_order(self):
        q = MultiQueue(weights=[1,5,3])
        for i in xrange(10):
            q.put((0,i))
        for i in xrange(10):
            q.put((1,i))
        for i in xrange(10):
            q.put((2,i))

        # check first in, first out
        self.assertEqual(q.get(),(0,0))
        self.assertEqual(q.get(),(1,0))
        self.assertEqual(q.get(),(2,0))
        
        # now weights start to affect results
        self.assertEqual(q.get(),(1,1))
        self.assertEqual(q.get(),(1,2))
        self.assertEqual(q.get(),(1,3))
        self.assertEqual(q.get(),(2,1))
        self.assertEqual(q.get(),(1,4))
        self.assertEqual(q.get(),(0,1))
        self.assertEqual(q.get(),(1,5))
        self.assertEqual(q.get(),(1,6))
        self.assertEqual(q.get(),(2,2))
        self.assertEqual(q.get(),(1,7))
        self.assertEqual(q.get(),(1,8))
        self.assertEqual(q.get(),(1,9))
        
        # no more items from queue 1
        self.assertEqual(q.get(),(2,3))
        self.assertEqual(q.get(),(0,2))
        self.assertEqual(q.get(),(2,4))
        self.assertEqual(q.get(),(0,3))
        self.assertEqual(q.get(),(2,5))
        self.assertEqual(q.get(),(2,6))
        self.assertEqual(q.get(),(0,4))
        self.assertEqual(q.get(),(2,7))
        self.assertEqual(q.get(),(2,8))
        self.assertEqual(q.get(),(0,5))
        self.assertEqual(q.get(),(2,9))
        
        # no more items from queue 2
        self.assertEqual(q.get(),(0,6))
        self.assertEqual(q.get(),(0,7))
        self.assertEqual(q.get(),(0,8))
        self.assertEqual(q.get(),(0,9))
    
    def test_auto_recycle(self):
        # very small value for auto_recycle, don't do this in real code
        q = MultiQueue(weights=[1,10], auto_recycle=100)
        
        # fill queues with some data
        q.put((0,1))
        q.put((1,1))
            
        # forces cycle to grow over auto_recycle value
        for i in xrange(20):
            q.put((0,1))
            q.put((1,1))
            q.get()
            q.get()
        
        # extract rest of items
        while not q.empty():
            q.get()
    
if __name__ == '__main__':
    unittest.main()
