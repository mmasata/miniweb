from miniweb.core.miniweb import log
from miniweb.exception.exception import *
from .content import get_content

class Request:
    """
    Class for HTTP request which store parameters in class attributes.
    """


    def __init__(self):
        self.headers = {}
        self.close = False
        self.content_read = False
        self.has_path = False


    async def parse_header(self, data):
        """
        Accept HTTP request header in raw and parse them and store to attribute.
        :param data: Incoming header row.
        :return: Boolean if we can continue read headers.
        """

        try:
            if not self.has_path:
                self.method, full_path, proto = data.split()
                log.info("Incoming HTTP request {m} {p}.".format(m=self.method, p=full_path))

                await self.__find_query_params(full_path)
                self.has_path = True
            else:
                header, value = data.split(": ")
                self.headers[header] = value.replace("\r\n", "")
                log.debug("Header\n {k}: {v}".format(k=header, v=self.headers[header]))

                if "Content-Length" == header:
                    self.headers["Content-Type"] = self.headers["Content-Type"].split(";")[0]
                    self.content_len = int(value)
                    self.content_read = self.content_len > 0
                    return False

            return True
        except HeaderException:
            log.error("Error during read of request headers!")


    async def parse_content(self, data):
        """
        Accept Content-Data and parse them to object. Object is stored to Request class.
        :param data: Incoming Content-Data
        :return: None
        """

        log.debug("Content data: \r\n"+data)
        try:
            self.content = get_content(data, self.headers["Content-Type"])
        except ContentTypeException:
            log.error("Error in parsing Content-Type!")


    async def __find_query_params(self, full_path):
        if "?" in full_path:
            log.debug("Parsing query params.")

            self.params = {}
            self.path, q_par_str = full_path.split("?", 1)

            q_par_arr = q_par_str.split("&")
            for par in q_par_arr:
                key, value = par.split("=")
                self.params[key] = value

                log.debug("Query param\n {k}: {v}".format(k=key, v=value))
        else:
            self.path = full_path
