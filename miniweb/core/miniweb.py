import logging
log = logging.getLogger("miniweb")


from miniweb.entity.middleware import validate, validate_consumes
from miniweb.core.server import Server
from miniweb.entity.route import Route, StaticRoute
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
            log.error("Attempt to create more than one instances of miniweb!")
        else:
            Miniweb.__inst = self
            self.config = Config.get_instance(par)
            self.routes = []

            self.__enable_log()


    def __enable_log(self):
        try:
            log.setLevel(self.config.log)
            log.info("Logging was enabled. Level: {l}".format(l=self.config.log))
        except:
            raise ConfigParamsException("Miniweb log level is missing!")


    def run(self):
        """
        Create Server object instance and run it.
        :return: None
        """

        log.debug("Miniweb send request to initialize Server.")
        Server.get_instance(self).init()


    def stop(self, ms=0):
        """
        Set action for stop server after delay
        :return: None
        """
        s = Server.get_instance(self)
        s.keep_run = False
        s.delay = int(ms)


    def static_router(self, root, path, controller=None):
        """
        Register static router to miniweb.
        :param root: Folder path inside of device.
        :param path: Path for route.
        :param controller: Group router to group and define path. (optional parameter)
        :return: None
        """

        log.info("Static file server was enabled in root: {r}.".format(r=root))
        self.routes.append(StaticRoute(root, path, controller))


    def __reg_route(self, path, methods, fc):
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
            res.status(404).type("text/html").entity(not_found(req.path, req.method)).build()
        else:
            if params is None:
                route.fc(req, res)
            else:
                route.fc(req, res, params)
        return res


    async def __find_route(self, req):
        for route in self.routes:
            if (req.method in route.methods) and (route.is_match(req.path)):
                params = route.get_path_params(req.path)
                log.info("Match with request and route was found.")
                log.debug("Request match with regex: {re}.".format(re=route.regex_str))
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
                log.debug("Route decorator accept function for path: p.".format(p=path))

                full_path = controller.path+path if controller is not None else path
                self.__reg_route(full_path, methods, wrapper)
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
            return self.route(path, ["GET"], controller, consumes)(fc)
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
            return self.route(path, ["POST"], controller, consumes)(fc)
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
            return self.route(path, ["PUT"], controller, consumes)(fc)
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
            return self.route(path, ["DELETE"], controller, consumes)(fc)
        return _inner
