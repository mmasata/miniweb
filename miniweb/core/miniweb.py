import logging
log = logging.getLogger("miniweb")


from miniweb.entity.middleware import validate, validate_consumes
from miniweb.core.server import server
from miniweb.utils.enumerators import Method, Status, Mime
from miniweb.entity.route import Route
from miniweb.message.response import Response
from miniweb.utils.templates import *
from miniweb.entity.config import config
from miniweb.exception.exception import *


# Trida Miniweb je singleton, proto vracime pres tuto metodu
def miniweb(params=None):
    return Miniweb.get_instance(params)

# Miniweb je kontejner pro cely framework, jedna se o singleton
class Miniweb:
    __instance = None

    # staticka metoda zajistujici singleton
    @staticmethod
    def get_instance(params=None):
        if Miniweb.__instance == None:
            Miniweb(params)
        return Miniweb.__instance

    def __init__(self, params=None):
        if Miniweb.__instance != None:
            log.error("Attempt to create more than one instances of miniweb.")
            raise SingletonExpcetion("Cannot create new instance of Miniweb class. Its Singleton.")
        else:
            self.config = config(params)
            Miniweb.__instance = self
            # pole, kde bude cela struktura routovani a reference na jednotlive metody
            self.routes = []
            #reference na jedinou instanci serveru
            self.server = None
            self.init_logging()

    #postara se o nastaveni loggeru
    def init_logging(self):
        try:
            log.setLevel(self.config.log)
            #predame do miniwebu
            log.info("Inicialize miniweb")
        except:
            raise ConfigParamsException("Miniweb log level is missing!")

    #metoda spusti server
    def run(self):
        log.debug("Miniweb send request to initialize Server.")
        self.server = server(self)

    #zaregistruje endpoint do mapy
    def register_route(self, path, methods, fc):
        self.routes.append(Route(path, methods, fc))


    #metoda, ktera se stara o navraceni responsu klientovi
    async def handle_response(self, req):
        route, params = await self.find_route(req)
        #pokud nenajde shodu, vracime 404
        res = Response()
        if route == None:
            return res.status(Status.NOT_FOUND).type(Mime.HTML).entity(not_found(req.path, req.method)).build()
        #pokud ma parametry predame do dekorovane funkce, v opacnem pripade nikoliv
        if params != None:
            route.fc(req, res, params)
        else:
            route.fc(req, res)
        return res

    #hleda route (a parametry) dle prijateho requestu
    async def find_route(self, req):
        for route in self.routes:
            #musi odpovidat jak metoda, tak cesta s regexem
            if req.method in route.methods:
                match, params = route.match_with_vars(req.path)
                if match:
                    log.info("Match with request and route was found.")
                    log.debug("Request match with regex: "+route.regex_str)
                    return route, params
        log.info("Route for request was not found.")
        return None, None


    #### Metody zajistujici dekoratory pro cestu endpointu a metody ####

    # Univerzalni route
    def route(self, path, methods, controller=None, consumes=None):
        log.debug("Route decorator accept function for path: "+path)
        def _route(fc):
            def wrapper(*args, **kwargs):
                result = None
                #volame middleware, posilame controller a referenci na request a response
                if (validate_consumes(consumes, args[0], args[1])) and (validate(controller, args[0], args[1])):
                    result = fc(*args, **kwargs)
                return result
            fullPath = controller.path+path if controller != None else path
            self.register_route(fullPath, methods, wrapper)
            return wrapper
        return _route

    # Get route
    def get(self, path, controller=None, consumes=None):
        def _inner(fc):
            return self.route(path, [Method.GET], controller, consumes)(fc)
        return _inner

    # Post route
    def post(self, path, controller=None, consumes=None):
        def _inner(fc):
            return self.route(path, [Method.POST], controller, consumes)(fc)
        return _inner

    # Put route
    def put(self, path, controller=None, consumes=None):
        def _inner(fc):
            return self.route(path, [Method.PUT], controller, consumes)(fc)
        return _inner

    # Delete route
    def delete(self, path, controller=None, consumes=None):
        def _inner(fc):
            return self.route(path, [Method.DELETE], controller, consumes)(fc)
        return _inner

