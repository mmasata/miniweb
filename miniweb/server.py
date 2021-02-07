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
        #TODO
        return 0

    #Zastavi server
    def stop(self):
        print("Vypinam server...")
        #TODO
        return 0

    # Odesle HTTP response
    def sendResponse(self):
        #TODO
        return 0