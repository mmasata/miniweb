from miniweb.core.miniweb import log
from miniweb.tools.enumerators import Mime
import ujson


def get_content(data, t):
    """
    Parse incoming Content-Type to object.
    :param data: Raw Content-Data from HTTP request.
    :param t: Content-Type of HTTP request Content-Data.
    :return: Data parsed to object.
    """
    result = data
    if t == Mime.JSON:
        log.info("Parsing JSON string to object.")
        result = ujson.loads(data)
    elif t == Mime.FormData:
        result = FormData(data)
    else:
        log.warning("Unknown content type! Content will be accessable in raw format.")
    return result

class Content():
    """
    Abstract class for Contents types.
    """

    def __init__(self, data):
        self.__parse_data(data)


    def __parse_data(self, data):
        pass


class FormData(Content):
    """
    Child of abstract class Content. This class wrapped form data and store them to class attributes.
    """

    def __parse_data(self, data):
        log.info("Parsing FormData.")
        rows = data.split("\r\n")
        read_values = False
        current_value = ""
        current_is_file = False
        filename = None
        current_key = None
        for row in rows:
            if not (row[0:2] == "--"):
                if not read_values:
                    if row != "":
                        param_header = row.split(";")
                        current_is_file = len(param_header) == 3
                        filename = param_header[2] if current_is_file else None
                        current_key = param_header[1].split('"')[1]
                        read_values = True
                else:
                    current_value += row
            elif current_key is not None:
                if current_is_file:
                    current_value = self.__create_file(filename, current_value)
                log.debug("Set form data attribute: "+current_key)
                setattr(self, current_key, current_value)
                read_values = False
                current_key = None
                current_value = ""
                filename = None


    def __create_file(self, filename, data):
        file_and_type = filename.replace('"', "").split(".")
        return File(file_and_type[0].split("=")[1], file_and_type[1], data)


class File:
    """
    Class for storing file with his data, name, type.
    """

    def __init__(self, name, type, data):
        self.name = name
        self.type = type
        self.data = data


    def get_data(self):
        """
        Getter for data.
        :return: File data
        """
        return self.data


    def get_type(self):
        """
        Getter for type.
        :return: File type
        """
        return self.type


    def get_name(self):
        """
        Getter for name.
        :return: File name
        """
        return self.name
