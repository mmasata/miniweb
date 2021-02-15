import micropython
import uasyncio as asyncio
from .http_message import Request
import gc

def server(miniweb):
    return Server.get_instance(miniweb)

class Server:
    __instance = None

    # staticka metoda zajistujici singleton
    @staticmethod
    def get_instance(miniweb):
        if Server.__instance == None:
            Server(miniweb)
        return Server.__instance

    def __init__(self, miniweb):
        if Server.__instance != None:
            raise Exception("Cannot create new instance of Server class. Its Singleton.")
        else:
            self.miniweb = miniweb
            self.params = self.miniweb.params
            self.log = self.miniweb.log
            #default file name
            self.file_name = "config.env"
        self.init()


    #Spusti server
    def init(self):
        #spusti garbage collector
        gc.collect()
        self.event_loop = asyncio.get_event_loop()
        self.event_loop.create_task(asyncio.start_server(self.handle, "localhost", self.params["port"]))
        self.log.info("Server is running on localhost port:"+str(self.params["port"]))
        self.event_loop.run_forever()

    #pracuje s inputem a outputem
    async def handle(self, reader, writer):
        req = Request(self.log)
        first_line = True
        reading_headers = True
        #headers budeme cist po radcich, protoze je stejne potrebujeme roztridit
        while reading_headers:
            header_line = await reader.readline()
            # zparsuje raw data do vhodnejsiho formatu
            header_line = header_line.decode()
            reading_headers = await req.parse_header(header_line, first_line)
            first_line = False
        #cteme content jako celek, neni potreba pracovat s radky
        if req.content_read:
            content = await reader.read()
            content = content.decode()
            await req.parse_content(content)
        res = await self.miniweb.handle_response(req)
        #request uz nas po zpracovani nezajima, uvolnujeme
        del req
        #pokud prijde None nezavirame, nechame klienta zavrit na timeout
        if res != None and res.can_send:
            await writer.awrite("HTTP/1.0 "+str(res.stat)+"\r\n")
            if res.ent != None or res.mime != None:
                await writer.awrite("Content-Type: "+res.mime+"\r\n")
                entity_len = str(len(res.ent))
                await writer.awrite("Content-Length: "+entity_len+"\r\n\r\n")
                await writer.awrite(res.ent)
            await writer.aclose()
        # po zpracovani a dokonceni response uvolnujeme
        del res

    #Zastavi server
    def stop(self):
        self.event_loop.close()

