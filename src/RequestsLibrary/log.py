import io

from robot.api import logger

from RequestsLibrary.utils import merge_headers


def log_response(method, response):
    # TODO big responses should be truncated to avoid huge logs
    logger.debug('%s Response : status=%s, reason=%s\n' % (method.upper(),
                                                           response.status_code,
                                                           response.reason) +
                 response.text)


def log_request(
        method,
        session,
        uri,
        **kwargs):

    # TODO would be nice to add also the alias
    # TODO would be nice to pretty format the headers / json / data
    # TODO move in common the data formatting to have this as @staticmethod
    # TODO big requests should be truncated to avoid huge logs

    # kwargs might include: method, session, uri, params, files, headers,
    #                       data, json, allow_redirects, timeout
    args = kwargs.copy()
    args.pop('session', None)
    # This will log specific headers merged with session defined headers
    merged_headers = merge_headers(session, args.pop('headers', None))
    formatted_data = format_data_to_log_string_according_to_headers(session,
                                                                    args.pop('data', None),
                                                                    merged_headers)
    formatted_json = args.pop('json', None)
    method_log = '%s Request using : ' % method.upper()
    uri_log = 'uri=%s' % uri
    composed_log = method_log + uri_log
    for arg in args:
        composed_log += ', %s=%s' % (arg, kwargs.get(arg, None))
    logger.info(composed_log + '\n' +
                'headers=%s \n' % merged_headers +
                'data=%s \n' % formatted_data +
                'json=%s' % formatted_json)


def format_data_to_log_string_according_to_headers(session, data, headers):
    data_str = None

    # when data is an open file descriptor we ignore it
    if data and isinstance(data, io.IOBase):
        return data_str

    # Merged headers are already case insensitive
    headers = merge_headers(session, headers)

    if data is not None and headers is not None and 'Content-Type' in headers:
        if (headers['Content-Type'].find("application/json") != -1) or \
                (headers['Content-Type'].find("application/x-www-form-urlencoded") != -1):
            if isinstance(data, bytes):
                data_str = data.decode('utf-8')
            else:
                data_str = data
        else:
            data_str = "<" + headers['Content-Type'] + ">"

    return data_str
