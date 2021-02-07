from functools import wraps
from .urlfunc import compile
from .middleware import *
from .server import server

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

    #zaregistruje endpoint do mapy
    def registerEndpoint(self, path, methods, fc):
        methodStr = "["+", ".join(methods)+"]"
        print("Registrace endpointu: "+path+" pro metody: "+methodStr)
        self.routes.append((compile(path), methods, fc))


    #### Metody zajistujici dekoratory pro cestu endpointu a metody ####

    # Univerzalni route
    def route(self, path, methods, controller=None):
        def _route(fc):
            fullPath = controller.path+path if controller != None else path
            self.registerEndpoint(fullPath, methods, fc)
            def wrapper(*args, **kwargs):
                result = None
                #volame middleware, posilame controller a referenci na request a response
                if validateFilters(controller, args[0], args[1]):
                    print("Middleware filtry prosli uspesne...")
                    result = fc(*args, **kwargs)
                return result
            return wrapper
        return _route

    # Get route
    def get(self, path, controller=None):
        def _inner(fc):
            return self.route(path, ["GET"], controller)(fc)
        return _inner

    # Post route
    def post(self, path, controller=None):
        def _inner(fc):
            return self.route(path, ["POST"], controller)(fc)
        return _inner

    # Put route
    def put(self, path, controller=None):
        def _inner(fc):
            return self.route(path, ["PUT"], controller)(fc)
        return _inner

    # Delete route
    def delete(self, path, controller=None):
        def _inner(fc):
            return self.route(path, ["DELETE"], controller)(fc)
        return _inner

    # Metoda zajistujici definici prijimanych a odesilanych datovych typu
    def media(self, consumes, produces):
        def _media(fc):
            def wrapper(*args, **kwargs):
                result = None
                # middleware kontrola spravnosti consumes
                if checkConsumeType(consumes, args[0]):
                    print("Consume type prosli uspesne...")
                    result = fc(*args, **kwargs)
                    #middleware kontrola produces, zda se jako HTTP response bude vracet spravny typ
                    if result != None:
                        if checkProduceType(produces, args[1]):
                            #TODO send response
                            print("Posilam response...")
                return result
            return wrapper
        return _media

