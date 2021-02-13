import ure

# Route je trida, kde jsou uchovany informace o metode, referenci na funkci dane route a parametry
class Route:

    def __init__(self, path, methods, fc):
        self.regex, self.param_keys = self.compile_regex(path)
        self.methods = methods
        self.fc = fc

    #zkompiluje String do regexu
    #vraci kompilovany regex a pole nazvu path variables
    def compile_regex(self, url):
        self.num_slashes = []
        slash = 0
        params = []
        current_param = ""
        path_param_reading = False
        for char in url:
            #kdyz mame zacinajici slozenou zavorku, zaciname cist jmeno parametru
            if char == "{":
                self.num_slashes.append(slash)
                path_param_reading = True
                continue
            #kdyz mame ukoncujici slozenou zavorku, prestavame cist jmeno parametru
            if char == "}":
                path_param_reading = False
                params.append(current_param)
                #nahradime v promenne regexu
                url = url.replace("{"+current_param+"}", "[a-zA-Z0-9]+")
                current_param = ""
                continue
            #pokud cteme parametr, pridavame char do stringu
            if path_param_reading:
                current_param += char
                continue
            if char == "/":
                slash += 1
                continue
        return ure.compile(url), params

    #vrati boolean zda sedi, a pokud jsou nejaky path params, pak doplni jejich hodnoty a take vrati
    def match_with_vars(self, path):
        match = ure.match(self.regex, path) != None
        params = None
        params_len = len(self.param_keys)
        if match and params_len > 0:
            path_len = len(path)
            params_found = 0
            params_dict = {}
            current_slash = 0
            path_param_value = ""
            for i in range(0, path_len):
                #lomitko mame jako oddelovac pro hledani hodnot path parametru
                if current_slash in self.num_slashes:
                    if path[i] != "/":
                        path_param_value += path[i]
                        if i == (path_len-1):
                            params_dict[self.param_keys[params_found]] = path_param_value
                    elif path[i] == "/" or i == iteration:
                        current_slash += 1
                        params_dict[self.param_keys[params_found]] = path_param_value
                        path_param_value = ""
                        params_found += 1
                        if params_found == params_len:
                            break
                elif path[i] == "/":
                    current_slash += 1
            params = params_dict
        return match, params
