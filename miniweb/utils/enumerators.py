from miniweb.core.miniweb import log

def get_mime_by_suffix(suff):
    log.debug("Incoming suffix to recognize Mime: "+suff)
    return suffix_file[suff]

#pro zapisovani hodnot, ktere jsou z omezeneho poctu moznosti pouzijeme Enumy

#Enumy pro logovaci urovne (prevzato z uloggeru, aby se to tam mohlo predat)
class Log:
    CRITICAL = 50
    ERROR = 40
    WARNING = 30
    INFO = 20
    DEBUG = 10
    NOTSET = 0

#Enum pro metody HTTP requestu
class Method:
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"

#Enum pro format souboru
class Mime:
    JSON = "application/json"
    FormData = "multipart/form-data"
    HTML = "text/html"
    CSS = "text/css"
    JS = "text/javascript"
    PLAIN = "text/plain"
    CSV = "text/csv"
    MD = "text/markdown"
    JPG = "image/jpeg"
    PNG = "image/png"
    BMP = "image/bmp"
    SVG = "image/svg+xml"


#Mapa pro suffix souboru a jejich content type
suffix_file = {
    "html": Mime.HTML,
    "htm": Mime.HTML,
    "css": Mime.CSS,
    "js": Mime.JS,
    "txt": Mime.PLAIN,
    "csv": Mime.CSV,
    "md": Mime.MD,
    "jpg": Mime.JPG,
    "jpeg": Mime.JPG,
    "png": Mime.PNG,
    "bmp": Mime.BMP,
    "svg": Mime.SVG
}


#Enum pro HTTP statusy
class Status:
    CONTINUE = 100
    SWITCHING_PROTOCOL = 101
    PROCESSING = 102
    EARLY_HINTS = 103
    OK = 200
    CREATED = 201
    ACCEPTED = 202
    NON_AUTHORITATIVE_INFORMATION = 203
    NO_CONTENT = 204
    RESET_CONTENT = 205
    PARTIAL_CONTENT = 206
    MULTI_STATUS = 207
    ALREADY_REPORTED = 208
    IM_USED = 226
    MULTIPLE_CHOICE = 300
    MOVED_PERMANENTLY = 301
    FOUND = 302
    SEE_OTHER = 303
    NOT_MODIFIED = 304
    USE_PROXY = 305
    UNUSED = 306
    TEMPORARY_REDIRECT = 307
    PERMANENT_REDIRECT = 308
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    PAYMENT_REQUIRED = 402
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    NOT_ACCEPTABLE = 406
    PROXY_AUTHENTICATION_REQUIRED = 407
    REQUEST_TIMEOUT = 408
    CONFLICT = 409
    GONE = 410
    LENGTH_REQUIRED = 411
    PRECONDITION_FAILED = 412
    PAYLOAD_TOO_LARGE = 413
    URI_TOO_LONG = 414
    UNSUPPORTED_MEDIA_TYPE = 415
    RANGE_NOT_SATISFIABLE = 416
    EXPECTATION_FAILED = 417
    IM_A_TEAPOT = 418
    MISDIRECTED_REQUEST = 421
    UNPROCESSABLE_ENTITY = 422
    LOCKED = 423
    FAILED_DEPENDENCY = 424
    TOO_EARLY = 425
    UPGRADE_REQUIRED = 426
    PRECONDITION_REQUIRED = 428
    TOO_MANY_REQUESTS = 429
    REQUEST_HEADER_FIELDS_TOO_LARGE = 431
    UNAVAILABLE_FOR_LEGAL_REASONS = 451
    INTERNAL_SERVER_ERROR = 500
    NOT_IMPLEMENTED = 501
    BAD_GATEWAY = 502
    SERVICE_UNAVAILABLE = 503
    GATEWAY_TIMEOUT = 504
    HTTP_VERSION_NOT_SUPPORTED = 505
    VARIANT_ALSO_NEGOTIATES = 506
    INSUFFICIENT_STORAGE = 507
    LOOP_DETECTED = 508
    NOT_EXTENDED = 510
    NETWORK_AUTHENTICATION_REQUIRED = 511


