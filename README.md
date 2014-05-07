python-multiqueue
=================

Sometimes when you use the Queue class in Python, you need to get an item from any of several queues.
This small module implements an easy solution for this problem.

MultiQueue class inherits from Queue and overrides internal methods of data access, 
sharing its interface but managing multiple queues instead of one.

To add items to a MultiQueue, the put method must receive a tuple with the identifier of the queue as the first element and the value to be stored as the second element.

When getting an item from a MultiQueue, you get a tuple indicating from which queue has been extracted and the extracted value.
If there are items in multiple queues, these are obtained mixed, as applying the Round Robin algorithm.

Furthermore, when instantiating the MultiQueue is possible to assign different weights to the queues, so that some have higher priority over others. 
If you have 2 queues in a MultiQueue, with weights 1 and 10 and both with a large number of elements, in 11 calls to get method you will obtain just one element from the first queue and 10 elements from the second.

A disadvantage of the approach used is that it is not possible to ask for items from a specific queue.
The other drawback is that every several operations, related to auto\_recycle constructor parameter, 
MultiQueue restarts internal counters to avoid reaching very high values, which slighty affects performance.

### Constructor ###
Receives some optional arguments:
- maxsize: maximum number of elements in any queue, 0 for infinite
- num\_queues: initial number of queues, by default is 0
- weights: list of positive integers with the weight of each queue
- allow\_resize: don't allow to put items on new queues ids; False by default is a num\_queues or a weights list, only can be True in other cases 
- auto\_recycle: frequency, on number of cycles, of restart counters operations, in most cases default value is adequate.

Examples:
    
    # An object with seven queues (ids 0 to 6) with different weights. 
    # Raises InvalidQueue when doing puts with another queue id.
    q = MultiQueue(maxsize=0, num_queues=7, weights=[1, 5, 2, 5, 1, 3, 10])
    
    # An object with no queues. 
    # For each different queue id in puts operation resizes the list of queues to allocate the new one.
    q = MultiQueue()

### Put ###
Put method receives a tuple (queue, item).

Example:

    q.put((5,{"any":"value","to":"put","in":"the queue"}))
    
### Get ###
Get returns a tuple (queue, item).

Example:

    # wait 1 second on a blocking get
    queue, value = q.get(True, timeout=1)
