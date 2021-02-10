#trida obalujici HTTP request
class Request:

    def __init__(self):
        print("Miniweb dostal request...")


    #prijata data jsou RAW, je treba je roztridit
    async def parse(self, data):
        #data prijdou v bytech, je treba je precodovat
        row_arr = data.decode().split("\r\n")
        row_arr_len = len(row_arr)
        for i in range(0, row_arr_len):
            if i == 0:
                #na zacatku dostaneme metodu, cestu a protokol
                self.method, self.path, self.protocol = row_arr[i].split()
        print("Request: Method nastavena na:"+self.method)
        print("Request: Path nastavena na: "+self.path)
        print("Request: Protocol nastaven na: "+self.protocol)
        #TODO rozparsovat na metodu, pathu, content type, content length a content


#trida obalujici HTTP response
class Response:

    def __init__(self):
        self.can_send = False



    #ulozi do instance status kod responsu
    def status(self, status):
        print("Definuji response status: "+str(status))
        self.status = status
        return self

    #ulozi do promenne data, ktera bude vracet v response
    def entity(self, data):
        print("Definuji response entity: "+data)
        self.entity = data
        return self

    #ulozi do promenne mime type, ktery bude response vracet
    def type(self, mime):
        print("Definuji response mime: "+mime)
        self.type = mime
        return self

    #zmeni boolean parametr na True, tim da najevo ze je response hotova k vraceni
    def build(self):
        self.can_send = True
        return self
