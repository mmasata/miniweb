import uasyncio as asyncio

def server(params=None):
    return Server.getInstance(params)

class Server:
    __instance = None

    # staticka metoda zajistujici singleton
    @staticmethod
    def getInstance(params=None):
        if Server.__instance == None:
            Server(params)
        return Server.__instance

    def __init__(self, params=None):
        if Server.__instance != None:
            raise Exception("Cannot create new instance of Server class. Its Singleton.")
        else:
            self.params = params if params != None else self.readParamsFromFile()
        self.init()

    # Vezme si env parametry ze souboru
    def readParamsFromFile(self):
        #TODO
        return 0

    #Spusti server
    def init(self):
        print("Inicializuji server na portu:"+str(self.params["port"]))
        self.event_loop = asyncio.get_event_loop()
        self.event_loop .create_task(asyncio.start_server(self.handle_request, "localhost", self.params["port"]))
        self.event_loop .run_forever()

    #zpracuje prichozi request
    async def handle_request(self, reader, writer):
        accept_data = await reader.read()
        print("Prijmuta data")
        print(accept_data)
        #TODO precte cely buffer a pak vytvori instanci requestu

        await writer.awrite("HTTP/1.0 200 OK\r\n")
        await writer.awrite("Content-Type: text/html\r\n")
        await writer.awrite("\r\n")
        await writer.awrite("<html><body><h1>Miniweb server works!</h1></body></html>")
        await writer.aclose()


    #Zastavi server
    def stop(self):
        print("Vypinam server...")
        self.event_loop.close()

    # Odesle HTTP response
    def sendResponse(self):
        #TODO
        return 0
