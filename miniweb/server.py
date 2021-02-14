import micropython
import uasyncio as asyncio
from .http_message import Request

def server(miniweb, params=None):
    return Server.get_instance(miniweb, params)

class Server:
    __instance = None

    # staticka metoda zajistujici singleton
    @staticmethod
    def get_instance(miniweb, params=None):
        if Server.__instance == None:
            Server(miniweb, params)
        return Server.__instance

    def __init__(self, miniweb, params=None):
        if Server.__instance != None:
            raise Exception("Cannot create new instance of Server class. Its Singleton.")
        else:
            self.params = params if params != None else self.get_params_from_config_file()
            self.miniweb = miniweb

            #default file name
            self.file_name = "config.env"
        self.init()

    # Vezme si env parametry ze souboru
    def get_params_from_config_file(self):
        #TODO
        return 0

    #Spusti server
    def init(self):
        self.event_loop = asyncio.get_event_loop()
        self.event_loop.create_task(asyncio.start_server(self.handle, "localhost", self.params["port"]))
        self.event_loop.run_forever()

    #pracuje s inputem a outputem
    async def handle(self, reader, writer):
        req = Request()
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
        #pokud prijde None nezavirame, nechame klienta zavrit na timeout
        if res != None and res.can_send:
            await writer.awrite("HTTP/1.0 "+str(res.stat)+"\r\n")
            if res.ent != None or res.mime != None:
                await writer.awrite("Content-Type: "+res.mime+"\r\n")
                entity_len = str(len(res.ent))
                await writer.awrite("Content-Length: "+entity_len+"\r\n\r\n")
                await writer.awrite(res.ent)
            await writer.aclose()


    #Zastavi server
    def stop(self):
        self.event_loop.close()
