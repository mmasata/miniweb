from miniweb.core.miniweb import log
from miniweb.exception.exception import *
from .content import *

#trida obalujici HTTP request
class Request:

    def __init__(self):
        self.headers = {}
        self.close = False

    async def parse_header(self, data, first=False):
        try:
            if first:
                # na zacatku dostaneme metodu, cestu a protokol
                self.method, full_path, proto = data.split()
                log.info("Incoming request "+self.method+" "+full_path)
                #protokol nas nezajima, uvolnime
                del proto

                await self.find_query_params(full_path)
            else:
                header, value = data.split(": ")
                value = value.replace("\r\n", "")
                log.debug("Header "+header+": "+value)
                self.headers[header] = value
                if "Content-Type" == header:
                    self.type = value.split(";")[0]
                elif "Content-Length" == header:
                    self.content_len = int(value)
                    self.content_read = True if self.content_len > 0 else False
                    return False
            return True
        except HeaderException:
            self.close = True


    async def parse_content(self, data):
        log.debug("Content data: \r\n"+data)
        try:
            self.content = get_content(data, self.type)
        except ContentTypeException:
            self.close = True

    #z cesty si vytahne query params a ulozi je do dictionary
    async def find_query_params(self, full_path):
        log.debug("Parsing query params.")
        if "?" in full_path:
            self.path, q_par_str = full_path.split("?", 1)
            q_par_arr = q_par_str.split("&")
            self.params = {}
            for par in q_par_arr:
                key, value = par.split("=")
                log.debug("Query param "+key+": "+value)
                self.params[key] = value
        else:
            self.path = full_path
