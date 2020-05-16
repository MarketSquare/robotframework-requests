from .RequestsOnSessionKeywords import RequestsOnSessionKeywords
from .version import VERSION

"""
RequestsLibrary (__init__ wrapper file)
|_ RequestsKeywords (common requests and sessionless keywords)
    |_ SessionKeywords (session creation and data)
        |_ DeprecatedKeywords (old keywords that need sessions)
        |_ RequestOnSessionKeywords (new keywords that use sessions)
"""


class RequestsLibrary(RequestsOnSessionKeywords):
    __version__ = VERSION
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
