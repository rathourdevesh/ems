"""Singleton class definition."""

class Singleton:
    """Class to create a Singleton object."""

    def __init__(self, klass):
        """Singleton __init__.

        args:
            klass (object): Python function object.
        """
        self.klass = klass
        self.instance = None

    def __call__(self, *args, **kwds):
        """Meta class call.

        returns:
            object: Returns self instance to calling class.
        """
        if self.instance is None:
            self.instance = self.klass(*args, **kwds)
        return self.instance