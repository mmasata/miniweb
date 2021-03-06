from miniweb.core.miniweb import log
from miniweb.tools.templates import *


global_filter = []


def filter(controller=None):
    """
    DECORATOR
    Register middleware function to miniweb container.
    :param controller: Group router to group and define path. (optional parameter)
    :return: None
    """

    def _filter(fc):
        if controller is None:
            log.debug("Adding new global middleware function.")
            global_filter.append(fc)
        else:
            log.debug("Adding new controller middleware function for controller with path: {p}".format(p=controller.path))
            controller.add_filter(fc)
        return fc
    return _filter


def validate(controller, req, res):
    """
    Validate incoming HTTP request - run middleware function.
    :param controller: Group router to group and define path. (optional parameter)
    :param req: HTTP request wrapped inside of Request class.
    :param res: Response class which will define HTTP response.
    :return: Boolean of success/fail.
    """

    log.info("Validate middlewares.")
    if not check_filters_group(global_filter, req, res):
        return False

    if controller is not None:
        if not check_filters_group(controller.filters, req, res):
            return False

    log.debug("Middleware function was suceed.")
    return True


def validate_consumes(mime, req, res):
    """
    Validate incoming Content-Type.
    :param mime: Mime type which route can accept.
    :param req: HTTP request wrapped inside of Request class.
    :param res:  Response class which will define HTTP response.
    :return: Boolean of success/fail.
    """

    log.info("Validate consumes.")
    if (mime is None) or (req.headers["Content-Type"] in mime):
        log.debug("Consumes middleware was suceed.")
        return True
    else:
        log.warning("Consumes middleware failed!")
        res.type("text/html").entity(consume_error(req.headers["Content-Type"])).status(400).build()
        return False


def check_filters_group(f_arr, req, res):
    """
    From array with function reference will run this functions.
    :param f_arr: Array of filter functions.
    :param req: HTTP request wrapped inside of Request class.
    :param res: Response class which will define HTTP response.
    :return: Boolean of success/fail.
    """

    for f in f_arr:
        result = f(req, res)
        if not result:
            log.warning("Middleware function {fc} failed.".format(fc=f.__name__))
            return False
    return True
