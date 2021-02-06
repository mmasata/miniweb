from functools import wraps
#from urlfunc import *
from .middleware import *

# Trida Miniweb je singleton, proto vracime pres tuto metodu
def start(port=None, params=None):
    return Miniweb.getInstance(port, params)

#trida Controlleru
class Controller:
    def __init__(self, path, params=None):
        self.path = path
        self.params = params

        #pole referenci na funkce pro middleware
        self.filters = []

    def addFilter(self, fc):
        self.filters.append(fc)


# Miniweb je kontejner pro cely framework, jedna se o singleton
class Miniweb:
    __instance = None

    # staticka metoda zajistujici singleton
    @staticmethod
    def getInstance(port=None, params=None):
        if Miniweb.__instance == None:
            Miniweb(port, params)
        return Miniweb.__instance

    def __init__(self, port, params=None):
        if Miniweb.__instance != None:
            raise Exception("Cannot create new instance of Miniweb class. Its Singleton.")
        else:
            Miniweb.__instance = self
            # port bezici aplikace
            self.port = port

            # dalsi env parametry
            self.params = params

            # pole, kde bude cela struktura routovani a reference na jednotlive metody
            self.routes = []

    #### Metody zajistujici dekoratory pro cestu endpointu a metody ####

    # Univerzalni route
    def route(self, path, methods, controller=None):
        def _route(fc):
            def wrapper(*args, **kwargs):
                result = None
                if validateFilters(controller):
                    print("Middleware filtry prosli uspesne...")
                    result = fc(*args, **kwargs)
                return result
            return wrapper
        return _route

    # Get route
    def get(self, path, controller=None):
        self.route(path, ['GET'], controller)
        def _get(fc):
            def wrapper(*args, **kwargs):
                result = None
                if validateFilters(controller):
                    print("Middleware filtry prosli uspesne...")
                    result = fc(*args, **kwargs)
                return result
            return wrapper
        return _get

    # Post route
    def post(self, path, controller=None):
        self.route(path, ['POST'], controller)
        def _post(fc):
            def wrapper(*args, **kwargs):
                result = None
                if validateFilters(controller):
                    print("Middleware filtry prosli uspesne...")
                    result = fc(*args, **kwargs)
                return result
            return wrapper
        return _post

    # Put route
    def put(self, path, controller=None):
        self.route(path, ['PUT'], controller)
        def _putRoute(fc):
            def wrapper(*args, **kwargs):
                result = None
                if validateFilters(controller):
                    print("Middleware filtry prosli uspesne...")
                    result = fc(*args, **kwargs)
                return result
            return wrapper
        return _putRoute

    # Delete route
    def delete(self, path, controller=None):
        self.route(path, ['DELETE'], controller)
        def _delete(fc):
            def wrapper(*args, **kwargs):
                result = None
                if validateFilters(controller):
                    print("Middleware filtry prosli uspesne...")
                    result = fc(*args, **kwargs)
                return result
            return wrapper
        return _delete

    # Metoda zajistujici definici prijimanych a odesilanych datovych typu
    def media(self, consumes, produces):
        def _media(fc):
            def wrapper(*args, **kwargs):
                result = None
                # middleware kontrola spravnosti consumes
                if checkConsumeType(consumes):
                    result = fc(*args, **kwargs)
                    #middleware kontrola produces, zda se jako HTTP response bude vracet spravny typ
                    if checkProduceType(produces):
                        #TODO send response
                        print("Posilam response...")
                return result
            return wrapper
        return _media

