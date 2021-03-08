from miniweb.core.miniweb import log
from miniweb.utils.enumerators import *
from miniweb.utils.templates import *
from miniweb.message.response import *

global_filter = []

def filter(controller=None):
    '''
    DECORATOR
    Register middleware function to miniweb container.
    :param controller: Group router to group and define path. (optional parameter)
    :return: None
    '''
    def _filter(fc):
        if controller == None:
            log.debug("Adding new global middleware function.")
            global_filter.append(fc)
        else:
            log.debug("Adding new controller middleware function for controller: "+controller.path)
            controller.add_filter(fc)
        return fc
    return _filter

def validate(controller, req, res):
    '''
    Validate incoming HTTP request - run middleware function.
    :param controller: Group router to group and define path. (optional parameter)
    :param req: HTTP request wrapped inside of Request class.
    :param res: Response class which will define HTTP response.
    :return: Boolean of success/fail.
    '''
    log.info("Validate middlewares.")
    if not check_filters_group(global_filter, req, res):
        return False
    if controller != None:
        if not check_filters_group(controller.filters, req, res):
            return False
    log.debug("Middleware function was suceed.")
    return True

def validate_consumes(mime, req, res):
    '''
    Validate incoming Content-Type.
    :param mime: Mime type which route can accept.
    :param req: HTTP request wrapped inside of Request class.
    :param res:  Response class which will define HTTP response.
    :return: Boolean of success/fail.
    '''
    log.info("Validate consumes.")
    if (mime is None) or (req.headers["Content-Type"] in mime):
        log.debug("Consumes middleware was suceed.")
        return True
    else:
        log.warning("Consumes middleware failed!")
        res.type(Mime.HTML).entity(consume_error(req.headers["Content-Type"])).status(Status.BAD_REQUEST).build()
        return False


def check_filters_group(filter_arr, req, res):
    '''
    From array with function reference will run this functions.
    :param filter_arr: Array of filter functions.
    :param req: HTTP request wrapped inside of Request class.
    :param res: Response class which will define HTTP response.
    :return: Boolean of success/fail.
    '''
    for filter in filter_arr:
        result = filter(req, res)
        if not result:
            log.warning("Middleware function failed: "+filter.__name__)
            return False
    return True
