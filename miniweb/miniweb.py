from .middleware import *
from .server import server
from .enumerators import *
from .route import Route
from .http_message import Response
from .html_template import *
from .string_operations import *

# Trida Miniweb je singleton, proto vracime pres tuto metodu
def miniweb():
    return Miniweb.get_instance()

# Miniweb je kontejner pro cely framework, jedna se o singleton
class Miniweb:
    __instance = None

    # staticka metoda zajistujici singleton
    @staticmethod
    def get_instance():
        if Miniweb.__instance == None:
            Miniweb()
        return Miniweb.__instance

    def __init__(self):
        if Miniweb.__instance != None:
            raise Exception("Cannot create new instance of Miniweb class. Its Singleton.")
        else:
            print("Inicializuji miniweb...")
            Miniweb.__instance = self
            # pole, kde bude cela struktura routovani a reference na jednotlive metody
            self.routes = []
            #reference na jedinou instanci serveru
            self.server = None

    #metoda spusti server
    #kdyz v params prijde None, budeme brat z config.env
    def run(self, params=None):
        self.server = server(self, params)

    #zaregistruje endpoint do mapy
    def register_route(self, path, methods, fc):
        self.routes.append(Route(path, methods, fc))


    #metoda, ktera se stara o navraceni responsu klientovi
    async def handle_response(self, req):
        route = await self.find_route(req)
        #pokud nenajde shodu, vracime 404
        if route == None:
            return Response().status(Status.NOT_FOUND).type(Mime.HTML).entity(not_found(req.path, req.method)).build()
        res = Response()
        route.fc(req, res)
        return res

    #hleda route dle prijateho requestu
    async def find_route(self, req):
        print("Hledam route...")
        for route in self.routes:
            #musi odpovidat jak metoda, tak cesta s regexem
            if req.method in route.methods and match(route.regex, req.path):
                return route
        return None


    #### Metody zajistujici dekoratory pro cestu endpointu a metody ####

    # Univerzalni route
    def route(self, path, methods, controller=None):
        def _route(fc):
            def wrapper(*args, **kwargs):
                result = None
                #volame middleware, posilame controller a referenci na request a response
                if validate(controller, args[0], args[1]):
                    print("Middleware filtry uspesne prosli...")
                    result = fc(*args, **kwargs)
                return result
            fullPath = controller.path+path if controller != None else path
            self.register_route(fullPath, methods, wrapper)
            return wrapper
        return _route

    # Get route
    def get(self, path, controller=None):
        def _inner(fc):
            return self.route(path, [Method.GET], controller)(fc)
        return _inner

    # Post route
    def post(self, path, controller=None):
        def _inner(fc):
            return self.route(path, [Method.POST], controller)(fc)
        return _inner

    # Put route
    def put(self, path, controller=None):
        def _inner(fc):
            return self.route(path, [Method.PUT], controller)(fc)
        return _inner

    # Delete route
    def delete(self, path, controller=None):
        def _inner(fc):
            return self.route(path, [Method.DELETE], controller)(fc)
        return _inner
