class FileException(Exception):
    """Exception for file operations"""
    pass


class SingletonExpcetion(Exception):
    """Exception for creating more than one instances of singleton class"""
    pass


class ConfigParamsException(Exception):
    """Exception for missing config parameters"""
    pass


class CompileRegexException(Exception):
    """Exception for compiling regex in route class"""
    pass


class HeaderException(Exception):
    """Request header exception"""
    pass


class ContentTypeException(Exception):
    """Request content type exception"""
    pass
