from robot.api import logger

from RequestsLibrary.utils import merge_headers, is_file_descriptor


def log_response(response):
    # TODO big responses should be truncated to avoid huge logs
    logger.debug("%s Response : url=%s \n " % (response.request.method.upper(),
                                               response.url) +
                 "status=%s, reason=%s \n " % (response.status_code,
                                               response.reason) +
                 "body=%s \n " % response.text)


def log_request(response):
    request = response.request
    if response.history:
        original_request = response.history[0].request
        redirected = '(redirected) '
    else:
        original_request = request
        redirected = ''
    logger.info("%s Request : " % request.method.upper() +
                "url=%s %s\n " % (original_request.url, redirected) +
                "path_url=%s \n " % original_request.path_url +
                "headers=%s \n " % request.headers +
                "body=%s \n " % request.body)


# TODO Currently unused
def format_data_to_log_string(data):

    if not data:
        return None

    if is_file_descriptor(data):
        return repr(data)

    return repr(data)


