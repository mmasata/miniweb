import uasyncio as asyncio
from miniweb.message.request import Request
from miniweb.message.response import Response
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

        res = await self.miniweb.handle_response(req, Response())
        log.debug("Response arrived back to server.py")

        if res is not None and res.can_send:
            await self.__send_headers(res, writer)
            await self.__send_data(res, writer)
            await writer.aclose()
            log.debug("Closing communication with client.")
        else:
            log.warning("End communication with client - will drop on timeout!")


    async def __send_headers(self, res, writer):
        log.debug("Sending response headers.")
        await writer.awrite("HTTP/1.1 "+str(res.stat)+"\r\n")
        await writer.awrite("Content-Type: "+res.mime+"\r\n\r\n")


    async def __send_data(self, res, writer):
        log.debug("Sending response data")
        if res.ent.__class__.__name__ == "TextIOWrapper":
            log.debug("Sending file/s.")
            b_arr = bytearray(res.buffer_size)

            while True:
                data = res.ent.readinto(b_arr)
                if not data:
                    break
                await writer.awrite(b_arr, 0, data)
        else:
            await writer.awrite(res.ent)


    def stop(self):
        """
        Stop uasyncio server.
        :return: None
        """
        log.info("Stopping server.")
        self.event_loop.close()
