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
        param_reading = False
        regex = ""
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
        return ure.compile(regex), params

    #vrati boolean zda sedi, a pokud jsou nejaky path params, pak doplni jejich hodnoty a take vrati
    def match_with_vars(self, path):
        match = ure.match(self.regex, path) != None
        params = None
        if match:
            params_len = len(self.param_keys)
            if params_len > 0:
                params = self.find_vars(path, params_len)
        return match, params

    #najde z cesty path parametry a priradi je k jejich nazvum - klic:value
    def find_vars(self, path, params_len):
        # nadefinujeme delku do promenne, abychom ji nemuseli pocitat kazdou iteraci
        path_len = len(path)
        params_found = current_slash = 0
        params = {}
        path_param_value = ""
        for i in range(0, path_len):
            # lomitko mame jako oddelovac pro hledani hodnot path parametru
            if current_slash in self.num_slashes:
                if path[i] != "/":
                    path_param_value += path[i]
                    # v pripade ze cela path konci parametrem, neni dale dalsi slash, proto je treba zapsat ihned
                    if i == (path_len - 1):
                        params[self.param_keys[params_found]] = path_param_value
                        break
                else:
                    params[self.param_keys[params_found]] = path_param_value
                    path_param_value = ""
                    params_found += 1
                    current_slash += 1
                    # pokud mame jiz vsechny parametry, nemusime pokracovat, koncime
                    if params_found == params_len:
                        break
            elif path[i] == "/":
                current_slash += 1
        return params
