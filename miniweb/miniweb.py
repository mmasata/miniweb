from .urlfunc import compile
from .middleware import *
from .server import server
from .enumerators import *

# Trida Miniweb je singleton, proto vracime pres tuto metodu
def miniweb():
    return Miniweb.getInstance()

# Miniweb je kontejner pro cely framework, jedna se o singleton
class Miniweb:
    __instance = None

    # staticka metoda zajistujici singleton
    @staticmethod
    def getInstance():
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

    #metoda spusti server
    #kdyz v params prijde None, budeme brat z env_file.json
    def run(self, params=None):
        self.server = server(params)
        return 0

    #zaregistruje endpoint do mapy
    def registerEndpoint(self, path, methods, fc):
        methodStr = "["+", ".join(methods)+"]"
        print("Registrace endpointu: "+path+" pro metody: "+methodStr)
        self.routes.append((compile(path), methods, fc))


    #### Metody zajistujici dekoratory pro cestu endpointu a metody ####

    # Univerzalni route
    def route(self, path, methods, controller=None):
        def _route(fc):
            def wrapper(*args, **kwargs):
                result = None
                #volame middleware, posilame controller a referenci na request a response
                if validateFilters(controller, args[0], args[1]):
                    print("Middleware filtry uspesne prosli...")
                    result = fc(*args, **kwargs)
                return result
            fullPath = controller.path+path if controller != None else path
            self.registerEndpoint(fullPath, methods, wrapper)
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