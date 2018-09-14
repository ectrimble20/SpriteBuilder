class Manager(object):
    """
    Fancy pants object manager

    Basically just a wrapper for a dict but gives you the option of assigning with dictionary
    Example:
        manager = Manager()
        manager.add('my_thing', object)     # add the object
        manager.get('my_thing')             # retrieve the object
        manager[my_thing]                   # access object
        manager[my_other_thing] = object    # add a new object
        for key, value in manager:
            print("{} - {}".format(key, value) # iterate on the managers objects
        manager.clear()                     # clear objects
    """

    def __init__(self):
        self._managed = {}

    def add(self, key, managed):
        self._managed[key] = managed

    def has(self, key):
        return key in self._managed.keys()

    def get(self, key, default=None):
        return self._managed.get(key, default)

    def clear(self):
        self._managed.clear()

    def items(self):
        return self._managed.items()

    def __getitem__(self, item):
        return self._managed.get(item, None)

    def __setitem__(self, key, value):
        self._managed[key] = value
