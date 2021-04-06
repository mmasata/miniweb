import ure
from miniweb.core.miniweb import log
from miniweb.exception.exception import *
from miniweb.tools.enumerators import get_mime_by_suffix, Status, Mime
from miniweb.tools.templates import *
from miniweb.entity.middleware import validate

class Route:
    """
    Route class. Contains path, HTTP methods and reference for route function.
    """


    def __init__(self, path, methods, fc):
        log.info("Register route for methods: ["+', '.join(methods)+"] and path:"+path)

        self.path = path
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
                if char is "{":
                    self.num_slashes.append(slash)
                    param_reading = True
                elif char is "}":
                    param_reading = False
                    params.append(current_param)
                    self.regex_str += "\w+"
                    current_param = ""
                elif param_reading:
                    current_param += char
                else:
                    self.regex_str += char
                    slash = slash+1 if char is "/" else slash

            self.regex_str += "$"
            return ure.compile(self.regex_str), params
        except:
            raise CompileRegexException("Error with compiling regex in route class!")


    def is_match(self, path):
        """
        Accept current path from HTTP request and looking for match with current route.
        :param path: Incoming path from HTTP request.
        :return: Boolean of match
        """

        log.debug("Looking for route match \r\n path: "+path+"\r\n reg: "+self.regex_str)
        return ure.match(self.regex, path) is not None


    def get_path_params(self, path):
        """
        Accept current path from HTTP request and try found path parameters.
        :param path: Incoming path from HTTP request.
        :return: path parameters in dictionary
        """

        params = None
        if len(self.param_keys) > 0:
            log.debug("Getting variables from path.")

            params = {}
            split_path = path.split("/")
            slash_arr_size = len(self.num_slashes)

            for i in range(0, slash_arr_size):
                params[self.param_keys[i]] = split_path[self.num_slashes[i]]

        return params


class StaticRoute(Route):
    """
    Static route is child of Route class. Define routes for device folder and server static files in device.
    """


    def __init__(self, root, path, controller=None):
        self.file_path = path if controller is None else controller.path+path
        self.root = root

        log.info("Creating static route.")

        def _inner(req, res):
            if validate(controller, req, res):
                res.status(Status.OK).type(self.mime).entity(self.file).build()

        super().__init__(path, "GET", _inner)


    def __compile_regex(self, url):
        try:
            self.regex_str = "^"+self.file_path+"\S+"
            return ure.compile(self.regex_str), []
        except:
            raise CompileRegexException("Error with compiling regex in static route class!")


    def is_match(self, path):
        try:
            destination_file = path.replace(self.file_path, self.root, 1)

            log.info("Looking for static file.")
            log.debug("Destination path should be: " + destination_file)

            self.file = open(destination_file)
            self.mime = get_mime_by_suffix(destination_file)
            return True
        except:
            log.debug("Match with static route was not found.")
            return False
