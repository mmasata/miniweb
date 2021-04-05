import logging
log = logging.getLogger("miniweb")


from miniweb.entity.middleware import validate, validate_consumes
from miniweb.core.server import Server
from miniweb.tools.enumerators import Method, Status, Mime
from miniweb.entity.route import Route, StaticRoute
from miniweb.message.response import Response
from miniweb.tools.templates import *
from miniweb.entity.config import Config
from miniweb.exception.exception import *

def app(par=None):
    """
    Return the Miniweb object instance.
    :param par: Dictionary with configuration parameters. (optional parameter)
    :return: Miniweb object instance.
    """
    return Miniweb.get_instance(par)


class Miniweb:
    """
    Singleton class. It is container for all other framework objects.
    """
    __inst = None


    @staticmethod
    def get_instance(par=None):
        """
        Static method of Miniweb class. Provides instance and ensure singleton pattern.
        :param par: Dictionary with configuration parameters. (optional parameter)
        :return: Miniweb object instance.
        """

        if Miniweb.__inst is None:
            Miniweb(par)
        return Miniweb.__inst


    def __init__(self, par=None):
        if Miniweb.__inst is not None:
            log.error("Attempt to create more than one instances of miniweb.")
        else:
            self.config = Config.get_instance(par)
            Miniweb.__inst = self
            self.routes = []
            self.__init_logging()


    def __init_logging(self):
        try:
            log.setLevel(self.config.log)
            log.info("Inicialize miniweb")
        except:
            raise ConfigParamsException("Miniweb log level is missing!")


    def run(self):
        """
        Create Server object instance and run it.
        :return: None
        """

        log.debug("Miniweb send request to initialize Server.")
        Server.get_instance(self)


    def static_router(self, root, path, controller=None):
        """
        Register static router to miniweb.
        :param root: Folder path inside of device.
        :param path: Path for route.
        :param controller: Group router to group and define path. (optional parameter)
        :return: None
        """

        log.info("Static file server was enabled in root: "+root)
        self.routes.append(StaticRoute(root, path, controller))


    def __register_route(self, path, methods, fc):
        log.debug("Constructor of Route class was called.")
        self.routes.append(Route(path, methods, fc))


    async def handle_response(self, req, res):
        """
        From request object find route and call route function. Return response.
        :param req: HTTP request wrapped inside of Request class.
        :return: Response object instance.
        """

        route, params = await self.__find_route(req)
        if route is None:
            return res.status(Status.NOT_FOUND).type(Mime.HTML).entity(not_found(req.path, req.method)).build()
        if params is not None:
            route.fc(req, res, params)
        else:
            route.fc(req, res)
        return res


    async def __find_route(self, req):
        for route in self.routes:
            if req.method in route.methods:
                match, params = route.match_with_vars(req.path)
                if match:
                    log.info("Match with request and route was found.")
                    log.debug("Request match with regex: "+route.regex_str)
                    return route, params
        log.info("Route for request was not found.")
        return None, None


    def route(self, path, methods, controller=None, consumes=None):
        """
        DECORATOR
        Register route to miniweb. General class method.
        :param path: Path for route.
        :param methods: Route HTTP methods defined in array.
        :param controller: Group router to group and define path. (optional parameter)
        :param consumes: Validation for incoming Content-Type. (optional parameter)
        :return: None
        """

        def _route(fc):
            def wrapper(*args, **kwargs):
                result = None
                if (validate_consumes(consumes, args[0], args[1])) and (validate(controller, args[0], args[1])):
                    result = fc(*args, **kwargs)
                return result

            if methods is not None and path is not None:
                log.debug("Route decorator accept function for path: " + path)
                fullPath = controller.path+path if controller is not None else path
                self.__register_route(fullPath, methods, wrapper)
            else:
                log.warning("Route path or method is None!")

            return wrapper
        return _route


    def get(self, path, controller=None, consumes=None):
        """
        DECORATOR
        Register route to miniweb. Predefined class method with HTTP method - GET.
        :param path: Path for route.
        :param controller: Group router to group and define path. (optional parameter)
        :param consumes: Validation for incoming Content-Type. (optional parameter)
        :return: None
        """

        def _inner(fc):
            return self.route(path, [Method.GET], controller, consumes)(fc)
        return _inner


    def post(self, path, controller=None, consumes=None):
        """
        DECORATOR
        Register route to miniweb. Predefined class method with HTTP method - POST.
        :param path: Path for route.
        :param controller: Group router to group and define path. (optional parameter)
        :param consumes: Validation for incoming Content-Type. (optional parameter)
        :return: None
        """

        def _inner(fc):
            return self.route(path, [Method.POST], controller, consumes)(fc)
        return _inner


    def put(self, path, controller=None, consumes=None):
        """
        DECORATOR
        Register route to miniweb. Predefined class method with HTTP method - PUT.
        :param path: Path for route.
        :param controller: Group router to group and define path. (optional parameter)
        :param consumes: Validation for incoming Content-Type. (optional parameter)
        :return: None
        """

        def _inner(fc):
            return self.route(path, [Method.PUT], controller, consumes)(fc)
        return _inner


    def delete(self, path, controller=None, consumes=None):
        """
        DECORATOR
        Register route to miniweb. Predefined class method with HTTP method - DELETE.
        :param path: Path for route.
        :param controller: Group router to group and define path. (optional parameter)
        :param consumes: Validation for incoming Content-Type. (optional parameter)
        :return: None
        """

        def _inner(fc):
            return self.route(path, [Method.DELETE], controller, consumes)(fc)
        return _inner
