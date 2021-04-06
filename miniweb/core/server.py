import uasyncio as asyncio
from miniweb.message.request import Request
from miniweb.message.response import Response
from miniweb.core.miniweb import log
from miniweb.exception.exception import *
import gc
import ujson


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


    def __init__(self, miniweb):
        if Server.__instance is not None:
            log.error("Cannot create new instance of Server class. Its Singleton.")
        else:
            self.miniweb = miniweb
            self.config = miniweb.config
            self.__init()


    def __init(self):
        gc.collect()
        server_task = None

        try:
            server_task = asyncio.start_server(self.__handle, self.config.host, self.config.port)
        except:
            raise ConfigParamsException("Host or port is missing!")

        log.info("Server is running on "+self.config.host+" port:"+str(self.config.port))

        e_loop = asyncio.get_event_loop()
        e_loop.create_task(server_task)
        e_loop.run_forever()


    async def __handle(self, reader, writer):
        req = Request()
        h_read = True

        while h_read:
            h_line = await reader.readline()

            if h_line == b"\r\n":
                log.debug("All headers was accepted.")
                break

            if len(h_line) > 0:
                h_read = await req.parse_header(h_line.decode())

        if req.content_read:
            content = await reader.read(-1)
            await req.parse_content(content.decode())

        res = await self.miniweb.handle_response(req, Response())
        log.debug("Response arrived back to server.py")

        if res is not None and res.can_send:
            await self.__send_headers(res, writer)
            await self.__send_data(res, writer)
            await self.__close_connection(writer)
        else:
            log.warning("End communication with client - will drop on timeout!")


    async def __send_headers(self, res, writer):
        log.debug("Sending response headers.")

        await writer.awrite("HTTP/1.1 "+str(res.stat)+"\r\n")
        await writer.awrite("Content-Type: "+res.mime+"\r\n\r\n")


    async def __send_data(self, res, writer):
        log.debug("Sending response data")

        d_type = res.ent.__class__.__name__
        if d_type == "TextIOWrapper":
            log.debug("Sending file/s.")

            b_arr = bytearray(self.config.buffer)
            while True:
                data = res.ent.readinto(b_arr)

                if not data:
                    break
                await writer.awrite(b_arr, 0, data)

        elif d_type == "dict":
            log.debug("Dumps dictionary to JSON string and sending to client.")

            json_str = ujson.dumps(res.ent)
            await writer.awrite(json_str)

        else:
            await writer.awrite(res.ent)


    async def __close_connection(self, writer):
        log.debug("Closing communication with client.")
        await writer.aclose()
