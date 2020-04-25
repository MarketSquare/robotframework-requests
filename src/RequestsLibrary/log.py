from robot.api import logger

from RequestsLibrary.utils import merge_headers, is_file_descriptor


def log_response(method, response):
    # TODO big responses should be truncated to avoid huge logs
    logger.debug('%s Response : status=%s, reason=%s\n' % (method.upper(),
                                                           response.status_code,
                                                           response.reason) +
                 response.text)


def log_request2(
        method,
        session,
        uri,
        **kwargs):

    # TODO would be nice to add also the alias
    # TODO would be nice to pretty format the headers / json / data
    # TODO big requests should be truncated to avoid huge logs

    # kwargs might include: method, session, uri, params, files, headers,
    #                       data, json, allow_redirects, timeout
    args = kwargs.copy()
    args.pop('session', None)
    # This will log specific headers merged with session defined headers
    merged_headers = merge_headers(session, args.pop('headers', None))
    formatted_data = format_data_to_log_string(args.pop('data', None))
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


def log_request(request):
    logger.info("%s Request : " % request.method.upper() +
                "url=%s \n " % request.url +
                "path_url=%s \n " % request.path_url +
                "headers=%s \n " % request.headers +
                "body=%s \n " % request.body)


def format_data_to_log_string(data):

    if not data:
        return None

    if is_file_descriptor(data):
        return repr(data)

    return repr(data)


