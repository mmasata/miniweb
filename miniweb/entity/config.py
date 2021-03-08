from miniweb.utils.enumerators import Log
from miniweb.exception.exception import *
import os

def config(params=None):
    '''
    Return the Config object instance.
    :param params: Dictionary with configuration parameters. (optional parameter)
    :return: Config object instance.
    '''
    return Config.get_instance(params)

class Config:
    '''
    Singleton class. Parse configuration parameters from dictionary or configuration file.
    '''
    __instance = None

    @staticmethod
    def get_instance(params=None):
        '''
        Static method of Config class. Provides instance and ensure singleton pattern.
        :param params: Dictionary with configuration parameters. (optional parameter)
        :return: Config object instance.
        '''
        if Config.__instance == None:
            Config(params)
        return Config.__instance

    def __init__(self, params=None):
        if Config.__instance != None:
            raise SingletonExpcetion("Cannot create new instance of Config class. Its Singleton.")
        else:
            Config.__instance = self
            if params == None:
                self.__get_params_from_config_file()
            else:
                self.__assign_variables(params)

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
            raise FileException("No config file was found!")
        self.__assign_variables(params)

    def __find_file(self):
        list = os.ilistdir()
        file_name = None
        for file in list:
            if file[0].endswith(".env"):
                file_name = file[0]
                break
        return file_name

    def __assign_variables(self, params):
        for key in params:
            setattr(self, key, params[key])
