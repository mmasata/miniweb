# Modul pro middleware funkce

#pole uchovavajici obecne middleware funkce
global_filter = []

#dekorator pro registraci middleware filtru
def filter(controller=None):
    def _filter(fc):
        if controller == None:
            print("Registruju globalni middleware funkci "+fc.__name__)
            global_filter.append(fc)
        else:
            print("Registruju middleware funkci pro controller "+controller.path+" "+fc.__name__)
            controller.add_filter(fc)
        return fc
    return _filter

# spusti vsechny middleware funkce a vrati boolean
def validate(controller, req, res):
    print("Kontrola global filtru...")
    if not check_filters_group(global_filter, req, res):
        return False
    if controller != None:
        print("Kontrola controller filtru...")
        if not check_filters_group(controller.filters, req, res):
            return False
    return True

def check_filters_group(filter_arr, req, res):
    for filter in filter_arr:
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
