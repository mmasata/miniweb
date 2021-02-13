# Modul pro middleware funkce

#pole uchovavajici obecne middleware funkce
global_filter = []

#dekorator pro registraci middleware filtru
def filter(controller=None):
    def _filter(fc):
        if controller == None:
            global_filter.append(fc)
        else:
            controller.add_filter(fc)
        return fc
    return _filter

# spusti vsechny middleware funkce a vrati boolean
def validate(controller, req, res):
    if not check_filters_group(global_filter, req, res):
        return False
    if controller != None:
        if not check_filters_group(controller.filters, req, res):
            return False
    return True

def check_filters_group(filter_arr, req, res):
    for filter in filter_arr:
        result = filter(req, res)
        if not result:
            return False
    return True
