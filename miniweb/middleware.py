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
def validateFilters(controller, req, res):
    print("Kontrola global filtru...")
    for filter in globalFilters:
        if not filter(req, res):
            return False
    if controller != None:
        print("Kontrola controller filtru...")
        for filter in controller.filters:
            if not filter(req, res):
                return False
    return True


# kontroluje zda prijaty datovy typ odpovida nastavenemu
def checkConsumeType(consumes, req):
    print("Kontrola consume type...")
    # TODO
    return True


# kontroluje zda odesilany datovy typ odpovida nastavenemu
def checkProduceType(produces, res):
    print("Kontrola produce type...")
    # TODO
    return True
