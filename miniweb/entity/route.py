import ure
from miniweb.core.miniweb import log
from miniweb.exception.exception import *

# Route je trida, kde jsou uchovany informace o metode, referenci na funkci dane route a parametry
class Route:

    def __init__(self, path, methods, fc):
        log.info("Register route for methods: ["+', '.join(methods)+"] and path:"+path)
        self.regex, self.param_keys = self.compile_regex(path)
        self.methods = methods
        self.fc = fc

    #zkompiluje String do regexu
    #vraci kompilovany regex a pole nazvu path variables
    def compile_regex(self, url):
        try:
            log.debug("Compile url to regex.")
            self.num_slashes = []
            slash = 0
            params = []
            current_param = ""
            param_reading = False
            regex = "^"
            for char in url:
                #kdyz mame zacinajici slozenou zavorku, zaciname cist jmeno parametru
                if char == "{":
                    self.num_slashes.append(slash)
                    param_reading = True
                    continue
                #kdyz mame ukoncujici slozenou zavorku, prestavame cist jmeno parametru
                if char == "}":
                    param_reading = False
                    params.append(current_param)
                    #nahradime v promenne regexu
                    regex += "\w+"
                    current_param = ""
                    continue
                #pokud cteme parametr, pridavame char do stringu
                if param_reading:
                    current_param += char
                    continue
                if char == "/":
                    slash += 1
                regex += char
            regex += "$"
            self.regex_str = regex
            return ure.compile(regex), params
        except:
            raise CompileRegexException("Error with compiling regex in route class!")

    #vrati boolean zda sedi, a pokud jsou nejaky path params, pak doplni jejich hodnoty a take vrati
    def match_with_vars(self, path):
        match = ure.match(self.regex, path) != None
        params = None
        if match:
            if len(self.param_keys) > 0:
                params = self.find_vars(path)
        return match, params

    # najde z cesty path parametry a priradi je k jejich nazvum - klic:value
    def find_vars(self, path):
        log.debug("Getting variables from path.")
        params = {}
        split_path = path.split("/")
        #zname pozice indexu splitu, kde jsou path variables
        slash_arr_size = len(self.num_slashes)
        for i in range(0, slash_arr_size):
            params[self.param_keys[i]] = split_path[self.num_slashes[i]]
        return params
