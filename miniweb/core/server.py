import uasyncio as asyncio
from miniweb.message.request import Request
from miniweb.core.miniweb import log
from miniweb.exception.exception import *
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
            raise SingletonExpcetion("Cannot create new instance of Server class. Its Singleton.")
        else:
            self.miniweb = miniweb
            self.config = miniweb.config
            self.__init()


    #Spusti server
    def __init(self):
        #spusti garbage collector
        gc.collect()
        port = None
        host = None
        try:
            port = self.config.port
            host = self.config.host
        except:
            raise ConfigParamsException("Host or port is missing!")
        self.event_loop = asyncio.get_event_loop()
        self.event_loop.create_task(asyncio.start_server(self.__handle, host, port))
        log.info("Server is running on "+self.config.host+" port:"+str(port))
        self.event_loop.run_forever()


    #pracuje s inputem a outputem
    async def __handle(self, reader, writer):
        req = Request()
        first_line = True
        reading_headers = True
        #headers budeme cist po radcich, protoze je stejne potrebujeme roztridit
        while reading_headers:
            header_line = await reader.readline()
            # zparsuje raw data do vhodnejsiho formatu
            if header_line == b"\r\n":
                log.debug("All headers was accepted.")
                break
            reading_headers = await req.parse_header(header_line.decode(), first_line)
            first_line = False
        #cteme content jako celek, neni potreba pracovat s radky
        if req.content_read:
            content = await reader.read()
            await req.parse_content(content.decode())
        res = await self.miniweb.handle_response(req)
        #pokud prijde None nezavirame, nechame klienta zavrit na timeout
        log.debug("Response arrived back to server.py")
        if res != None and res.can_send:
            data_to_send = "HTTP/1.1 "+str(res.stat)+"\r\n"
            if res.ent != "" and res.mime != "":
                data_to_send += "Content-Type: "+res.mime+"\r\nContent-Length: "+str(len(res.ent))+"\r\n\r\n"+res.ent
            await writer.awrite(data_to_send)
            log.debug("Closing communication with client.")
            await writer.aclose()
        else:
            log.warning("End communication with client - will drop on timeout!")


    #Zastavi server
    def stop(self):
        log.info("Stopping server.")
        self.event_loop.close()

