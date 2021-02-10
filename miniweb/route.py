from .string_operations import *

# Route je trida, kde jsou uchovany informace o metode, referenci na funkci dane route a parametry
class Route:

    def __init__(self, path, methods, fc):
        self.regex = compile_regex(path)
        self.methods = methods
        self.fc = fc
        methodStr = "["+", ".join(methods)+"]"
        print("Registrace endpointu: "+path+" pro metody: "+methodStr)
        # TODO
