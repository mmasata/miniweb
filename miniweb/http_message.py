#trida obalujici HTTP request
class Request:

    def __init__(self):
        print("Miniweb dostal request...")


    #prijata data jsou RAW, je treba je roztridit
    async def parse(self, data):
        #self.method
        #self.path
        #TODO rozparsovat na metodu, pathu, content type, content length a content
        return 0


#trida obalujici HTTP response
class Response:

    def __init__(self):
        self.can_send = false

    #ulozi do instance status kod responsu
    def status(self, status):
        self.status = status
        return self

    #ulozi do promenne data, ktera bude vracet v response
    def entity(self, data):
        self.data = data
        return self

    #ulozi do promenne mime type, ktery bude response vracet
    def type(self, mime):
        self.mime = mime

    #zmeni boolean parametr na True, tim da najevo ze je response hotova k vraceni
    def build(self):
        self.can_send = True
