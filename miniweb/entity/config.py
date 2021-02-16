from miniweb.core.miniweb import log
from miniweb.utils.enumerators import Log
import os

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
        else:
            Config.__instance = self
            if params == None:
                self.get_params_from_config_file()
            else:
                self.assign_variables(params)

    # Vezme si env parametry ze souboru
    # nejdrive musi najit env soubor v projektu
    def get_params_from_config_file(self):
        f = open(self.find_file())
        data_arr = (f.read()).split("\n")
        params = {}
        for row in data_arr:
            if "=" in row:
                key, value = row.split("=")
                params[key] = value if key != "log" else self.asociate_debug_level(value)
        self.assign_variables(params)


    #najde ke Stringu spravnou log level hodnotu
    def asociate_debug_level(self, level):
        if level == "DEBUG":
            return Log.DEBUG
        if level == "INFO":
            return Log.INFO
        if level == "WARNING":
            return Log.WARNING
        if level == "ERROR":
            return Log.ERROR
        if level == "CRITICAL":
            return Log.CRITICAL
        return Log.NOTSET

    #oskenuje soubory a vrati ten prvni co nalezne s .env priponou
    def find_file(self):
        list = os.ilistdir()
        file_name = None
        for file in list:
            if ".env" in file[0]:
                file_name = file[0]
                break
        return file_name

    #priradi promenne
    def assign_variables(self, params):
        #pokud neni host nastaven, default bude "127.0.0.1"
        self.host = "127.0.0.1" if params["host"] == None else params["host"]
        #pokud neni port nastaven, default je 8080
        self.port = 8080 if params["port"] == None else params["port"]
        self.log = params["log"]
        #TODO
