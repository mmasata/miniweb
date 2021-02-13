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

    #nastavi cestu k env file
    def set_config_file_name(self, name):
        self.file_name = name

    # Vezme si env parametry ze souboru
    def get_params_from_config_file(self):
        #TODO
        return 0

    #Spusti server
    def init(self):
        self.event_loop = asyncio.get_event_loop()
        self.event_loop .create_task(asyncio.start_server(self.handle, "localhost", self.params["port"]))
        self.event_loop .run_forever()

    #pracuje s inputem a outputem
    async def handle(self, reader, writer):
        #micropython.mem_info()
        accept_data = await reader.read()
        req = Request()
        #zparsuje raw data do vhodnejsiho formatu
        await req.parse(accept_data)
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
