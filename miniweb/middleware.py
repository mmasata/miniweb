# Modul pro middleware funkce

#pole uchovavajici obecne middleware funkce
globalFilters = []

#dekorator pro registraci middleware filtru
def filter(controller=None):
    def _filter(fc):
        if controller == None:
            print("Registruju globalni middleware funkci "+fc.__name__)
            globalFilters.append(fc)
        else:
            print("Registruju middleware funkci pro controller "+controller.path+" "+fc.__name__)
            controller.addFilter(fc)
        return fc
    return _filter

# spusti vsechny middleware funkce a vrati boolean
def validateFilters(controller, req, res):
    print("Kontrola global filtru...")
    if not checkFilters(globalFilters, req, res):
        return False
    if controller != None:
        print("Kontrola controller filtru...")
        if not checkFilters(controller.filters, req, res):
            return False
    return True

def checkFilters(filterArr, req, res):
    for filter in filterArr:
        result = filter(req, res)
        if not result:
            if res == None:
                print("Ukonceni http dotazu, bez zadne response...")
                return False
            else:
                print("Ukonceni http dotazu, zasilam response")
                #TODO
                return False
    return True
