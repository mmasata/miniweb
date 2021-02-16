from miniweb.core.miniweb import log
#trida Controlleru
class Controller:
    def __init__(self, path, params=None):
        log.debug("Creating of new controller: "+path)
        self.path = path
        self.params = params

        #pole referenci na funkce pro middleware
        self.filters = []

    #ulozi si referenci na filter funkci controlleru
    def add_filter(self, fc):
        self.filters.append(fc)
