from miniweb.utils.enumerators import Log
from miniweb.exception.exception import *
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
            #nelze zalogovat, v tuto chvili neni vytvoreny logger
            raise SingletonExpcetion("Cannot create new instance of Config class. Its Singleton.")
        else:
            Config.__instance = self
            if params == None:
                self.__get_params_from_config_file()
            else:
                self.__assign_variables(params)

    # Vezme si env parametry ze souboru
    # nejdrive musi najit env soubor v projektu
    def __get_params_from_config_file(self):
        params = {}
        try:
            f = open(self.__find_file())
            data_arr = (f.read()).split("\n")
            for row in data_arr:
                if "=" in row:
                    key, value = row.split("=")
                    params[key] = value if key != "log" else getattr(Log, value)
        except:
            #nebyl nalezen soubor, nebo z nej nelze cist
            #nelze zalogovat, v tuto chvili neni jeste nadefinovan logger
            raise FileException("No config file was found!")
        self.__assign_variables(params)


    #oskenuje soubory a vrati ten prvni co nalezne s .env priponou
    def __find_file(self):
        list = os.ilistdir()
        file_name = None
        for file in list:
            if file[0].endswith(".env"):
                file_name = file[0]
                break
        return file_name

    #priradi promenne
    def __assign_variables(self, params):
        for key in params:
            setattr(self, key, params[key])
