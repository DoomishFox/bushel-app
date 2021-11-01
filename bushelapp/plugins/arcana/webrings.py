from ..plugins import Plugin

class Webrings(Plugin):
    """This plugin is an implementation of Webrings 2.0 for bushel's
    parser module system. It adds a dynamic set of webring links from
    Arcana Labs' Webrings 2.0 server.
    """
    def __init__(self):
        super().__init__()
        self.description = 'Webrings 2.0 integration'

    def parse(self, context):
        """The actual implementation of the webrings plugin is to just return the
        argument
        """
        return context