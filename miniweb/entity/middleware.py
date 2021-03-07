from miniweb.core.miniweb import log
from miniweb.utils.enumerators import *
from miniweb.utils.templates import *
from miniweb.message.response import *
# Modul pro middleware funkce

#pole uchovavajici obecne middleware funkce
global_filter = []

#dekorator pro registraci middleware filtru
def filter(controller=None):
    def _filter(fc):
        if controller == None:
            log.debug("Adding new global middleware function.")
            global_filter.append(fc)
        else:
            log.debug("Adding new controller middleware function for controller: "+controller.path)
            controller.add_filter(fc)
        return fc
    return _filter

# spusti vsechny middleware funkce a vrati boolean
def validate(controller, req, res):
    log.info("Validate middlewares.")
    if not check_filters_group(global_filter, req, res):
        return False
    if controller != None:
        if not check_filters_group(controller.filters, req, res):
            return False
    log.debug("Middleware function was suceed.")
    return True

def validate_consumes(mime, req, res):
    log.info("Validate consumes")
    if (mime is None) or (req.headers["Content-Type"] in mime):
        log.debug("Consumes middleware was suceed.")
        return True
    else:
        log.warning("Consumes middleware failed!")
        res.type(Mime.HTML).entity(consume_error(req.headers["Content-Type"])).status(Status.BAD_REQUEST).build()
        return False


def check_filters_group(filter_arr, req, res):
    for filter in filter_arr:
        result = filter(req, res)
        if not result:
            log.warning("Middleware function failed: "+filter.__name__)
            return False
    return True
