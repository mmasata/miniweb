#trida obalujici HTTP request
class Request:

    def __init__(self, log):
        self.headers = {}
        self.log = log

    async def parse_header(self, data, first=False):
        if first:
            # na zacatku dostaneme metodu, cestu a protokol
            self.method, full_path, proto = data.split()
            self.log.info("Incoming request "+self.method+" "+full_path)
            #protokol nas nezajima, uvolnime
            del proto

            await self.find_query_params(full_path)
        else:
            header, value = data.split(": ")
            value = value.replace("\r\n", "")
            self.log.debug("Header "+header+": "+value)
            self.headers[header] = value
            if "Content-Type" == header:
                self.type = value
            elif "Content-Length" == header:
                self.content_len = int(value)
                self.content_read = True
                return False
        return True

    async def parse_content(self, data):
        self.content = data

    #z cesty si vytahne query params a ulozi je do dictionary
    async def find_query_params(self, full_path):
        if "?" in full_path:
            self.path, q_par_str = full_path.split("?", 1)
            q_par_arr = q_par_str.split("&")
            self.params = {}
            for par in q_par_arr:
                key, value = par.split("=")
                self.params[key] = value
        else:
            self.path = full_path


#trida obalujici HTTP response
class Response:

    def __init__(self, log):
        self.log = log
        self.can_send = False
        self.stat = None
        self.mime = None
        self.ent = None


    #ulozi do instance status kod responsu
    def status(self, status):
        self.log.debug("Response status was set to "+str(status))
        self.stat = status
        return self

    #ulozi do promenne data, ktera bude vracet v response
    def entity(self, data):
        self.ent = data
        return self

    #ulozi do promenne mime type, ktery bude response vracet
    def type(self, mime):
        self.mime = mime
        return self

    #zmeni boolean parametr na True, tim da najevo ze je response hotova k vraceni
    def build(self):
        self.log.info("Sending response with status:"+str(self.stat)+" and type:"+self.mime)
        self.can_send = True
        return self
