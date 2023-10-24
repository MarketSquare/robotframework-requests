import logging

from RequestsLibrary.utils import is_file_descriptor
from robot.api import logger


LOG_CHAR_LIMIT = 10000


def log_response(response):
    logger.info("%s Response : url=%s \n " % (response.request.method.upper(),
                                              response.url) +
                "status=%s, reason=%s \n " % (response.status_code,
                                              response.reason) +
                "headers=%s \n " % response.headers +
                "body=%s \n " % format_data_to_log_string(response.text))


def log_request(response, log_headers=False):
    request = response.request
    response_history = response.history
    original_request = response_history[0].request if response_history else request
    redirected = '(redirected) ' if response_history else ''
    headers = original_request.headers if log_headers else '{}'
    logger.info("%s Request : " % original_request.method.upper() +
                "url=%s %s\n " % (original_request.url, redirected) +
                "path_url=%s \n " % original_request.path_url +
                "headers=%s \n " % headers +
                "body=%s \n " % format_data_to_log_string(original_request.body))


def format_data_to_log_string(data, limit=LOG_CHAR_LIMIT):

    if not data:
        return None

    if is_file_descriptor(data):
        return repr(data)

    if logging.getLogger().level > logging.DEBUG and len(data) > limit:
        data = "%s... (set the log level to DEBUG or TRACE to see the full content)" % data[:limit]

    return data
