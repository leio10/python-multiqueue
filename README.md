python-multiqueue
=================

Allows to wait for multiple queues with a single object. Employs weighted round-robin as scheduling algorithm.

Queues are identified by ids, that are used on Put and Get operations. 

- Constructor receives some optional arguments.
 - maxsize: maximum number of elements in any queue, 0 for infinite
 - num\_queues: initial number of queues, by default is 0
 - weights: list of positive integers with the weight of each queue
 - allow\_resize: don't allow to put items on new queues ids; False by default is a num\_queues or a weights list, only can be True in other cases 
 - auto\_recycle: frequency, on number of cycles, of restart counters operations, default value used to be right in most cases 
       
    # An object with seven queues (ids 0 to 6) with different weights. Raises InvalidQueue when doing puts with another queue id.
    q = MultiQueue(maxsize=0, num\_queues=7, weights=[1, 5, 2, 5, 1, 3, 10])

    # An object with no queues. For each different queue id in puts operation resizes the list of queues to allocate the new one.
    q = MultiQueue()
    
- Put method receives a tuple (queue, item):
    
    q.put((5,{"any":"value","to":"put","in":"the queue"}))
    
- Get returns a tuple (queue, item).

    # wait 1 second on a blocking get
    queue, value = q.get(True, timeout=1000)
