import logging

from RequestsLibrary.utils import is_file_descriptor
from robot.api import logger


LOG_CHAR_LIMIT = 10000


def log_response(response):

    try:
        # Passing large body to format_data_to_log_string and
        # doing the len() of it takes a lot of time and causes high CPU usage.
        # If body size can be determined from header's 'Content-length' and body
        # size is larger then the limit, body will not be logged
        data_len = response.headers.get('Content-length')
        if int(data_len) > LOG_CHAR_LIMIT and logging.getLogger().level > 10:
            data = None
        else:
            data = response.text
    except:
        data = response.text

    logger.info("%s Response : url=%s \n " % (response.request.method.upper(),
                                              response.url) +
                "status=%s, reason=%s \n " % (response.status_code,
                                              response.reason) +
                "headers=%s \n " % response.headers +
                "body=%s \n " % format_data_to_log_string(data))


def log_request(response):
    request = response.request
    if response.history:
        original_request = response.history[0].request
        redirected = '(redirected) '
    else:
        original_request = request
        redirected = ''
    logger.info("%s Request : " % original_request.method.upper() +
                "url=%s %s\n " % (original_request.url, redirected) +
                "path_url=%s \n " % original_request.path_url +
                "headers=%s \n " % original_request.headers +
                "body=%s \n " % format_data_to_log_string(original_request.body))


def format_data_to_log_string(data, limit=LOG_CHAR_LIMIT):

    if not data:
        return None

    if is_file_descriptor(data):
        return repr(data)

    if len(data) > limit and logging.getLogger().level > 10:
        data = "%s... (set the log level to DEBUG or TRACE to see the full content)" % data[:limit]

    return data
