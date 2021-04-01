from miniweb.core.miniweb import log

class Controller:
    """
    Controller class groups routes.
    Define them prefix in path and define middleware function only for controller routes.
    """
    def __init__(self, path, params=None):
        if path is None:
            path = "/default/"
        log.debug("Creating new controller: "+path)
        self.path = path
        self.params = params
        self.filters = []

    def add_filter(self, fc):
        """
        Save reference to middleware function which belongs to Controller.
        :param fc: Function reference.
        :return: None
        """
        if fc is None:
            log.warning("Filter function is None!")
        else:
            self.filters.append(fc)
