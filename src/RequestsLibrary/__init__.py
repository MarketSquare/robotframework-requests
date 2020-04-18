from .RequestsKeywords import RequestsKeywords
from .version import VERSION


class RequestsLibrary(RequestsKeywords):
    __version__ = VERSION
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
