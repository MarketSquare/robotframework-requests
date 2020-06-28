import logging
import hashlib

from RequestsLibrary.utils import is_file_descriptor
from robot.api import logger


LOG_CHAR_LIMIT = 10000


def log_response(response):
    logger.info("%s Response : url=%s \n " % (response.request.method.upper(),
                                              response.url) +
                "status=%s, reason=%s \n " % (response.status_code,
                                              response.reason) +
                "body=%s \n " % format_data_to_log_string(response.text))


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
                "headers=%s \n " % redact_secure_header(original_request.headers) +
                "body=%s \n " % format_data_to_log_string(original_request.body))


def format_data_to_log_string(data, limit=LOG_CHAR_LIMIT):

    if not data:
        return None

    if is_file_descriptor(data):
        return repr(data)

    if len(data) > limit and logging.getLogger().level > 10:
        data = "%s... (set the log level to DEBUG or TRACE to see the full content)" % data[:limit]

    return data


def redact_secure_header(header):
    """Redact the secure headers to be logged."""
    secure_headers = ('authorization', 'x-auth-token',
                      'x-subject-token', 'x-service-token')
    for key in header.keys():
        if key.lower() in secure_headers:
            token_hasher = hashlib.sha256()
            token_hasher.update(header[key].encode('utf-8'))
            token_hash = token_hasher.hexdigest()
            header[key] = '{SHA256}%s' % token_hash
    return header
