from .DeprecatedKeywords import DeprecatedKeywords
from .RequestsOnSessionKeywords import RequestsOnSessionKeywords
from .version import VERSION

"""
** Inheritance structure **
RequestsKeywords (common requests and sessionless keywords)
    |_ SessionKeywords (session creation and data)
        |_ DeprecatedKeywords (old keywords that need sessions)
        |_ RequestsOnSessionKeywords (new keywords that use sessions)
        
RequestsLibrary (extends RequestsOnSessionKeywords, DeprecatedKeywords)
"""


class RequestsLibrary(RequestsOnSessionKeywords, DeprecatedKeywords):
    __version__ = VERSION
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
