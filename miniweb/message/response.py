from miniweb.core.miniweb import log

class Response:
    """
    Response class for building HTTP response.
    """


    def __init__(self):
        self.can_send = False
        self.stat = 500
        self.mime = None
        self.ent = None


    def status(self, status):
        """
        Set HTTP status to Response.
        :param status: HTTP status code.
        :return: self
        """

        log.debug("Response status was set to {s}.".format(s=status))
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

        log.debug("Response type was set to {m}.".format(m=mime))
        self.mime = mime
        return self


    def build(self):
        """
        Send response to client and mark it as finished.
        :return: self
        """

        log.debug("Response was marked as builded.")
        self.can_send = True
        return self
