from miniweb.core.miniweb import log

class Response:
    """
    Response class for building HTTP response.
    """

    def __init__(self):
        self.can_send = False
        self.stat = 500
        self.mime = ""
        self.ent = ""


    def status(self, status):
        """
        Set HTTP status to Response.
        :param status: HTTP status code.
        :return: self
        """
        log.debug("Response status was set to "+str(status))
        self.stat = status
        return self


    def entity(self, data):
        """
        Set response data.
        :param data: Response data.
        :return: self
        """
        self.ent = data
        return self


    def type(self, mime):
        """
        Set MIME type to Response.
        :param mime: Response data type.
        :return: self
        """
        log.debug("Response type was set to "+mime)
        self.mime = mime
        return self


    def build(self):
        """
        Mark Response class as ready for send.
        :return: self
        """
        log.info("Building response with status:"+str(self.stat)+" and type:"+self.mime)
        self.can_send = True
        return self
