# Modul pro middleware funkce

#pole uchovavajici obecne middleware funkce
globalFilters = []

#dekorator pro registraci middleware filtru
def filter(controller=None):
    def _filter(fc):
        if controller == None:
            print("Registruju globalni middleware funkci...")
            globalFilters.append(fc)
        else:
            print("Registruju middleware funkci pro controller "+controller.path)
            controller.addFilter(fc)
        return fc
    return _filter

# spusti vsechny middleware funkce a vrati boolean
def validateFilters(controller):
    if controller != None:
        for filter in controller.filters:
            if not filter():
                return False
    # do filters for all routes
    # TODO
    return True


# kontroluje zda prijaty datovy typ odpovida nastavenemu
def checkConsumeType(consumes):
    # TODO
    return True


# kontroluje zda odesilany datovy typ odpovida nastavenemu
def checkProduceType(produces):
    # TODO
    return True
