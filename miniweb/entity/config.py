from miniweb.tools.enumerators import Log
from miniweb.exception.exception import *
import os


class Config:
    """
    Singleton class. Parse configuration parameters from dictionary or configuration file.
    """
    __instance = None

    @staticmethod
    def get_instance(params=None):
        """
        Static method of Config class. Provides instance and ensure singleton pattern.
        :param params: Dictionary with configuration parameters. (optional parameter)
        :return: Config object instance.
        """
        if Config.__instance is None:
            Config(params)
        return Config.__instance

    def __init__(self, params=None):
        if Config.__instance is not None:
            raise SingletonExpcetion("Cannot create new instance of Config class. Its Singleton.")
        else:
            Config.__instance = self
            if params is None:
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
                    params[key] = value if key is not "log" else getattr(Log, value)
        except:
            raise FileException("No config file was found!")
        self.__assign_variables(params)

    def __find_file(self):
        ld = os.ilistdir()
        fn = None
        for f in ld:
            if f[0].endswith(".env"):
                fn = f[0]
                break
        return fn

    def __assign_variables(self, par):
        for key in par:
            setattr(self, key, par[key])
