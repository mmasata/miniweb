from miniweb.core.miniweb import log
from miniweb.utils.enumerators import Mime
import ujson

#metoda najde podle content type prislusneho potomka tridy Content a vytvori jeho instanci a vrati
def get_content(data, type):
    result = data
    if type == Mime.JSON:
        log.info("Parsing JSON.")
        result = ujson.loads(data)
    elif type == Mime.FormData:
        result = FormData(data)
    else:
        log.warning("Unknown content type!")
    return result


#Trida obsahujici objekt contentu z http requestu
class Content():

    def __init__(self, data):
        self.parse_data(data)

    #obecna metoda ktera bude prepisovana potomky
    def parse_data(self, data):
        pass


class FormData(Content):

    def parse_data(self, data):
        log.info("Parsing FormData.")
        rows = data.split("\r\n")
        read_values = False
        current_value = ""
        current_is_file = False
        filename = None
        current_key = None
        for row in rows:
            #nezajima nas boundary informace
            if not (row[0:2] == "--"):
                #kdyz necteme hodnoty, tak nas nezajimaji prazdne radky
                if not read_values:
                    if row == "":
                        continue
                    param_header = row.split(";")
                    current_is_file = len(param_header) == 3
                    filename = param_header[2] if current_is_file else None
                    current_key = param_header[1].split('"')[1]
                    read_values = True
                else:
                    current_value += row
            elif current_key is not None:
                if current_is_file:
                    current_value = self.create_file(filename, current_value)
                #ulozime do teto instance do parametru s nazvem ze vstupu
                setattr(self, current_key, current_value)
                read_values = False
                current_key = None
                current_value = ""
                filename = None

    def create_file(self, filename, data):
        file_and_type = filename.split(".")
        return File(file_and_type[0], file_and_type[1], data)


class File:

    def __init__(self, name, type, data):
        self.name = name
        self.type = type
        self.data = data

