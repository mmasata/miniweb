from miniweb.core.miniweb import log

def config(params=None):
    return Config.get_instance(params)

# Singleton trida, kde budou uchovany environment parametry miniwebu
class Config:
    __instance = None

    # staticka metoda zajistujici singleton
    @staticmethod
    def get_instance(params=None):
        if Config.__instance == None:
            Config(params)
        return Config.__instance

    #budto prijdou parametry z parametru, pokud ne bude se scanovat projekt a hledat soubor s priponou .env
    def __init__(self, params=None):
        if Config.__instance != None:
            raise Exception("Cannot create new instance of Config class. Its Singleton.")
            log.error("Attempt to create more than one instances of config.")
        else:
            if params == None:
                self.get_params_from_config_file()
            else:
                self.assign_variables(params)

    # Vezme si env parametry ze souboru
    # nejdrive musi najit env soubor v projektu
    def get_params_from_config_file(self):
        # TODO
        return 0

    #priradi promenne
    def assign_variables(self, params):
        #pokud neni port nastaven, default je 8080
        self.port = 8080 if params["port"] == None else params["port"]
        self.log = params["log"]
        #TODO
