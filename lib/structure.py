class Node(object):

    def __init__(self, data, next_node=None):
        self.data = data
        self.next_node = next_node


class LinkedList(object):

    def __init__(self):
        self._head = None
        self._tmp = None

    def is_empty(self):
        return self._head is None

    def __len__(self):
        c = 0
        n = self._head
        while n is not None:
            n = n.next_node
            c += 1
        return c

    def __iter__(self):
        self._tmp = self._head
        return self

    def __next__(self):
        t = self._tmp
        if t is None:
            self._tmp = None  # reset
            raise StopIteration
        else:
            self._tmp = self._tmp.next_node
            return t.data

    @property
    def first(self):
        return self._head

    @property
    def last(self):
        n = self._head
        if n is None:
            return None
        while n.next_node is not None:
            n = n.next_node
        return n

    def add(self, value):
        if self._head is None:              # check if a lead element is set
            self._head = Node(value, None)  # set lead element to new node holding new value
            return                          # return
        n = self._head                      # set lead element
        p = None                            # assign place holder for 'previous'
        while True:                         # search for end node
            if n is None:                   # if node is empty
                p.next_node = Node(value)   # assign next node to new node holding new value
                break                       # break loop, we're done
            else:
                p = n                       # assign previous to current node
                n = n.next_node             # not the last node, move to the next node

    def after(self, check, value):
        n = self._head                      # set lead element
        s = Node(value, None)               # set new node to hold new value
        while n is not None:                # loop on nodes
            if n.data == check:             # if node is our match
                s.next_node = n.next_node   # assign existing nodes next node as next node for new node
                n.next_node = s             # assign new node to existing nodes next node
                break                       # break loop, we're done
            else:
                n = n.next_node             # no match found, move to next node

    def before(self, check, value):
        n = self._head                      # set lead element
        p = None                            # assign place holder for 'previous'
        s = Node(value, None)               # set new node to hold new value
        while n is not None:                # loop on nodes
            if n.data == check:             # if node is our match
                s.next_node = n             # assign new node's next as current node
                if p is None:               # if previous is empty
                    self._head = s          # assign lead element as new element
                else:                       # otherwise
                    p.next_node = s         # assign previous's next node as new node
                break                       # break loop, we're done
            else:
                p = n                       # assign previous as this node
                n = n.next_node             # no match found, move to next node

    def delete(self, check):
        n = self._head
        p = None
        while n is not None:
            if n.data == check:
                if p is None:
                    self._head = n.next_node
                else:
                    p.next_node = n.next_node
                break
            else:
                p = n
                n = n.next_node

    def copy(self):
        c = LinkedList()
        for n in self:
            c.add(n)
        return c


class Pair(object):

    def __init__(self, first, second):
        self.first = first
        self.second = second
