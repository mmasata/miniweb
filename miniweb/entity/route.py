import ure
from miniweb.core.miniweb import log
from miniweb.exception.exception import *
from miniweb.utils.enumerators import get_mime_by_suffix, Status, Mime
from miniweb.utils.templates import *
from miniweb.entity.middleware import validate

# Route je trida, kde jsou uchovany informace o metode, referenci na funkci dane route a parametry
class Route:

    def __init__(self, path, methods, fc):
        log.info("Register route for methods: ["+', '.join(methods)+"] and path:"+path)
        self.regex, self.param_keys = self.__compile_regex(path)
        self.methods = methods
        self.fc = fc

    #zkompiluje String do regexu
    #vraci kompilovany regex a pole nazvu path variables
    def __compile_regex(self, url):
        try:
            log.debug("Compile url to regex.")
            self.num_slashes = []
            slash = 0
            params = []
            current_param = ""
            param_reading = False
            self.regex_str = "^"
            for char in url:
                #kdyz mame zacinajici slozenou zavorku, zaciname cist jmeno parametru
                if char == "{":
                    self.num_slashes.append(slash)
                    param_reading = True
                #kdyz mame ukoncujici slozenou zavorku, prestavame cist jmeno parametru
                elif char == "}":
                    param_reading = False
                    params.append(current_param)
                    #nahradime v promenne regexu
                    self.regex_str += "\w+"
                    current_param = ""
                #pokud cteme parametr, pridavame char do stringu
                elif param_reading:
                    current_param += char
                else:
                    self.regex_str += char
                    slash = slash+1 if char == "/" else slash
            self.regex_str += "$"
            return ure.compile(self.regex_str), params
        except:
            raise CompileRegexException("Error with compiling regex in route class!")

    #vrati boolean zda sedi, a pokud jsou nejaky path params, pak doplni jejich hodnoty a take vrati
    def match_with_vars(self, path):
        match = ure.match(self.regex, path) != None
        params = None
        if match:
            if len(self.param_keys) > 0:
                params = self.__find_vars(path)
        return match, params

    # najde z cesty path parametry a priradi je k jejich nazvum - klic:value
    def __find_vars(self, path):
        log.debug("Getting variables from path.")
        params = {}
        split_path = path.split("/")
        #zname pozice indexu splitu, kde jsou path variables
        slash_arr_size = len(self.num_slashes)
        for i in range(0, slash_arr_size):
            params[self.param_keys[i]] = split_path[self.num_slashes[i]]
        return params


#Route pro staticke servirovani
class Static_route(Route):

    def __init__(self, root, path, controller=None):
        self.file_path = path if controller is None else controller.path+path
        log.info("Creating static route.")
        def find_file(req, res):
            if validate(controller, req, res):
                try:
                    log.info("Looking for static file.")
                    destination_file = req.path.replace(self.file_path, root, 1)
                    log.debug("Destination path should be: "+destination_file)
                    f = open(destination_file)
                    f_data = f.read()
                    suff = destination_file.split('.')[1]
                    mime = get_mime_by_suffix(suff)
                    res.status(Status.OK).type(mime).entity(f_data).build()
                except:
                    log.warning("File was not found!")
                    res.status(Status.NOT_FOUND).type(Mime.HTML).entity(file_not_found(req.path)).build()
        super().__init__(path, "GET", find_file)

    def __compile_regex(self, url):
        try:
            self.regex_str = "^"+self.file_path+"\S+"
            return ure.compile(self.regex_str), []
        except:
            raise CompileRegexException("Error with compiling regex in static route class!")

