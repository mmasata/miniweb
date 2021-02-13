#trida Controlleru
class Controller:
    def __init__(self, path, params=None):
        #print("Vytvoreni controlleru "+path)
        self.path = path
        self.params = params

        #pole referenci na funkce pro middleware
        self.filters = []

    #ulozi si referenci na filter funkci controlleru
    def add_filter(self, fc):
        self.filters.append(fc)
