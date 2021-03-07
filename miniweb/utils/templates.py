def not_found(path, method):
    return "The requested URL "+path+" with method "+method+" was not found."

def consume_error(type):
    return "HTTP request contains bad content-type: "+type

def file_not_found(path):
    return "File with path of: "+path+" was not found."
