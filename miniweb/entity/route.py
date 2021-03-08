import ure
from miniweb.core.miniweb import log
from miniweb.exception.exception import *
from miniweb.utils.enumerators import get_mime_by_suffix, Status, Mime
from miniweb.utils.templates import *
from miniweb.entity.middleware import validate

class Route:
    '''
    Route class. Contains path, HTTP methods and reference for route function.
    '''
    def __init__(self, path, methods, fc):
        log.info("Register route for methods: ["+', '.join(methods)+"] and path:"+path)
        self.regex, self.param_keys = self.__compile_regex(path)
        self.methods = methods
        self.fc = fc

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
                if char == "{":
                    self.num_slashes.append(slash)
                    param_reading = True
                elif char == "}":
                    param_reading = False
                    params.append(current_param)
                    self.regex_str += "\w+"
                    current_param = ""
                elif param_reading:
                    current_param += char
                else:
                    self.regex_str += char
                    slash = slash+1 if char == "/" else slash
            self.regex_str += "$"
            return ure.compile(self.regex_str), params
        except:
            raise CompileRegexException("Error with compiling regex in route class!")

    def match_with_vars(self, path):
        '''
        Accept current path from HTTP request and looking for match with current route.
        If found try also found path parameters.
        :param path: Incoming path from HTTP request.
        :return: Boolean of match; path parameters in dictionary
        '''
        match = ure.match(self.regex, path) != None
        params = None
        if match:
            if len(self.param_keys) > 0:
                params = self.__find_vars(path)
        return match, params

    def __find_vars(self, path):
        log.debug("Getting variables from path.")
        params = {}
        split_path = path.split("/")
        slash_arr_size = len(self.num_slashes)
        for i in range(0, slash_arr_size):
            params[self.param_keys[i]] = split_path[self.num_slashes[i]]
        return params

class Static_route(Route):
    '''
    Static route is child of Route class. Define routes for device folder and server static files in device.
    '''

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
