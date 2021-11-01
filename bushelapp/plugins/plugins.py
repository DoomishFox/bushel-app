from ..database import db_session

class Plugin(object):
    """Base class that each plugin must inherit from. within this class
    you must define the methods that all of your plugins must implement
    """

    def __init__(self):
        self.name = 'plugin name'
        self.func = 'mod'
        self.db = db_session
        self.description = 'UNKNOWN'

    def parse(self, context):
        """The method that we expect all plugins to implement. This is the
        method that our framework will call
        """
        raise NotImplementedError