"""
    multiqueue.multiqueue
~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2012 by Leonardo Diez.
:license: BSD, see LICENSE for more details.
"""
from collections import deque
from Queue import Queue
from heapq import heappop, heappush, heappushpop

class InvalidQueue(Exception):
    "Exception raised by Queue.put() when using an invalid queue id and allow_resize=False."
    pass

class MultiQueue(Queue):
    """
    Variant of Queue that allow to handle multiple queues with the same object.
    
    Put method receives a tuple (queue, item) and Get returns a tuple (queue, item).
    
    When calling Put, if queue is bigger than num_queues:
        if allow_resize is True, resizes the list of queues to allocate the new one
        else, raises an InvalidQueue exception.
    """
    def __init__(self, maxsize=0, num_queues=None, weights=None, allow_resize=False, auto_recycle=0xFFFFFFF):
        """ Create a new MultiQueue.
        
        maxsize -- maximum number of elements in any queue
        num_queues -- initial number of queues
        weights -- list of positive integers with the weight of each queue, bigger is more important
        allow_resize -- False by default is a num_queues or a weights list, only can be True in other cases 
        """
        Queue.__init__(self, maxsize)
        
        # empty object
        self.num_queues = self.size = self.order_number = self.cycle = 0
        self.queues = []
        self.sizes = []
        self.active_queues = []
        self.wait = []
        
        # initialize queues arrays and weights 
        if weights:
            num_queues = len(weights)            
        elif num_queues:
            weights = [1]*num_queues
        
        if num_queues:
            self.wait = weights
            self.max_weight = max(self.wait)
            self._resize_queues(num_queues)
            self.wait = [self.max_weight-w+1 for w in self.wait] # converts weights in waiting times
            self.allow_resize = allow_resize
        else:
            self.max_weight = 1
            # without number of queues or a weights array, must allow queues resize
            self.allow_resize = True
        self.auto_recycle = auto_recycle
        
    def _init(self, maxsize):
        pass
        
    def _resize_queues(self, num_queues):
        if num_queues<=self.num_queues:
            self.queues = self.queues[0:num_queues]
            self.sizes = self.sizes[0:num_queues]
            self.wait = self.wait[0:num_queues]
        else:
            self.queues = self.queues + [deque() for i in xrange(self.num_queues,num_queues)]
            self.sizes = self.sizes + [0 for i in xrange(self.num_queues,num_queues)]
            self.wait.extend([self.max_weight]*(num_queues-len(self.wait)))
        self.num_queues = num_queues
        
    def _qsize(self, len=len):
        return self.size
        
    def _put(self, item):
        # item must be a queue id and a value to put
        queue, value = item
        
        # check if queue id is valid and resize or fails if not 
        if queue>=self.num_queues:
            if self.allow_resize:
                self._resize_queues(queue+1)
            else:
                raise InvalidQueue()
        
        # increment order number
        self.order_number += 1
        
        # auto recycle
        if self.cycle>self.auto_recycle:
            # update the active queues and queues values 
            self.active_queues = [(int(cycle-self.cycle), order-self.order_number, aqueue) for cycle, order, aqueue in self.active_queues]
            self.queues = [deque((order-self.order_number, value) for order, value in aqueue) for aqueue in self.queues]
        
            # reset values
            self.cycle = self.order_number = 0

        # if queue was empty add it to active queues
        if self.sizes[queue]==0:
            heappush(self.active_queues, (self.cycle+1, self.order_number, queue))
        
        # update sizes
        self.sizes[queue]+=1
        self.size+=1
        
        # append item to queue
        self.queues[queue].appendleft((self.order_number, value))

    def _get(self):
        # choose active queue
        self.cycle, order, queue = self.active_queues[0]
        
        # extract item from queue
        order, item = self.queues[queue].pop()

        # update sizes
        self.sizes[queue]-=1
        self.size-=1
        
        # if queue still has elements add it again to active queues, waiting 
        if self.sizes[queue]>0:
            heappushpop(self.active_queues, (self.cycle+self.wait[queue], self.queues[queue][0][0], queue))
        else:
            heappop(self.active_queues)
        return (queue, item)
