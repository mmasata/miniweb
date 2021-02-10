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
            self.file_name = "env_file.json"
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
        print("Inicializuji server na portu:"+str(self.params["port"]))
        self.event_loop = asyncio.get_event_loop()
        self.event_loop .create_task(asyncio.start_server(self.handle, "localhost", self.params["port"]))
        self.event_loop .run_forever()

    #pracuje s inputem a outputem
    async def handle(self, reader, writer):
        accept_data = await reader.read()
        req = Request()
        #zparsuje raw data do vhodnejsiho formatu
        await req.parse(accept_data)
        res = await self.miniweb.handle_response(req)
        #pokud prijde None nezavirame, nechame klienta zavrit na timeout
        if res != None and res.can_send:
            print("Odesilam response klientovi...")
            print("Status: "+str(res.status))
            print("Content-Type: "+res.type)
            await writer.awrite("HTTP/1.0 "+str(res.status)+"\r\n")
            await writer.awrite("Content-Type: "+res.type+"\r\n")
            if res.entity != None:
                entity_len = str(len(res.entity))
                await writer.awrite("Content-Length: "+entity_len+"\r\n\r\n")
                #await writer.awrite("\r\n")
                await writer.awrite(res.entity)
            await writer.aclose()


    #Zastavi server
    def stop(self):
        print("Vypinam server...")
        self.event_loop.close()
