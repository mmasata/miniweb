def not_found(path, method):
    return "The requested URL {p} with method {m} was not found.".format(p=path, m=method)


def consume_error(type):
    return "HTTP request has bad Content-Type: {t}".format(t=type)


def file_not_found(path):
    return "File with path {p} was not found.".format(p=path)

