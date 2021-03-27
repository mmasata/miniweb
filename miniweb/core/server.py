import uasyncio as asyncio
from miniweb.message.request import Request
from miniweb.core.miniweb import log
from miniweb.exception.exception import *
import gc


class Server:
    """
    Singleton class. Run uasyncio and handle HTTP request/response and send it to miniweb.
    """
    __instance = None

    @staticmethod
    def get_instance(miniweb):
        """
        Static method of Server class. Provides instance and ensure singleton pattern.
        :param params: Reference to instance of Miniweb class.
        :return: Server object instance.
        """
        if Server.__instance is None:
            Server(miniweb)
        return Server.__instance

    def __init__(self, miniweb):
        if Server.__instance is not None:
            log.error("Cannot create new instance of Server class. Its Singleton.")
        else:
            self.miniweb = miniweb
            self.config = miniweb.config
            self.__init()

    def __init(self):
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

    async def __handle(self, reader, writer):
        req = Request()
        first_line = True
        reading_headers = True
        while reading_headers:
            header_line = await reader.readline()
            if header_line == b"\r\n":
                log.debug("All headers was accepted.")
                break
            reading_headers = await req.parse_header(header_line.decode(), first_line)
            first_line = False
        if req.content_read:
            content = await reader.read(-1)
            await req.parse_content(content.decode())
        res = await self.miniweb.handle_response(req)
        log.debug("Response arrived back to server.py")
        if res is not None and res.can_send:
            data_to_send = "HTTP/1.1 "+str(res.stat)+"\r\n"
            if res.ent != "" and res.mime != "":
                data_to_send += "Content-Type: "+res.mime+"\r\nContent-Length: "+str(len(res.ent))+"\r\n\r\n"+res.ent
            await writer.awrite(data_to_send)
            log.debug("Closing communication with client.")
            await writer.aclose()
        else:
            log.warning("End communication with client - will drop on timeout!")

    def stop(self):
        """
        Stop uasyncio server.
        :return: None
        """
        log.info("Stopping server.")
        self.event_loop.close()

