from miniweb.core.miniweb import log


#trida obalujici HTTP response
class Response:

    def __init__(self):
        self.can_send = False
        self.stat = None
        self.mime = None
        self.ent = None


    #ulozi do instance status kod responsu
    def status(self, status):
        log.debug("Response status was set to "+str(status))
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
        log.info("Building response with status:"+str(self.stat)+" and type:"+self.mime)
        self.can_send = True
        return self
