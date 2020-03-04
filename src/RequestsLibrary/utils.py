import json
import types


from requests.status_codes import codes
from requests.structures import CaseInsensitiveDict

from RequestsLibrary.exceptions import UnknownStatusError
from RequestsLibrary.compat import urlencode, PY3


def parse_named_status(status_code):
    """
    Converts named status from human readable to integer
    """
    code = status_code.lower().replace(' ', '_')
    code = codes.get(code)
    if not code:
        raise UnknownStatusError(status_code)
    return code


def merge_headers(session, headers):
    if headers is None:
        headers = {}
    if session.headers is None:
        merged_headers = {}
    else:
        # Session headers are the default but local headers
        # have priority and can override values
        merged_headers = session.headers.copy()

    # Make sure merged_headers are CaseIsensitiveDict
    if not isinstance(merged_headers, CaseInsensitiveDict):
        merged_headers = CaseInsensitiveDict(merged_headers)

    merged_headers.update(headers)
    return merged_headers


def is_json(data):
    try:
        json.loads(data)
    except (TypeError, ValueError):
        return False
    return True


def json_pretty_print(content):
    """
    Pretty print a JSON object

    ``content``  JSON object to pretty print
    """
    temp = json.loads(content)
    return json.dumps(
        temp,
        sort_keys=True,
        indent=4,
        separators=(
            ',',
            ': '))


def is_string_type(data):
    if PY3 and isinstance(data, str):
        return True
    elif not PY3 and isinstance(data, unicode):
        return True
    return False


def utf8_urlencode(data):
    if is_string_type(data):
        return data.encode('utf-8')

    if not isinstance(data, dict):
        return data

    utf8_data = {}
    for k, v in data.items():
        if is_string_type(v):
            v = v.encode('utf-8')
        utf8_data[k] = v
    return urlencode(utf8_data)


def format_data_to_log_string_according_to_headers(session, data, headers):
    data_str = None
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


def format_data_according_to_header(session, data, headers):
    # Merged headers are already case insensitive
    headers = merge_headers(session, headers)

    if data is not None and headers is not None and 'Content-Type' in headers and not is_json(data):
        if headers['Content-Type'].find("application/json") != -1:
            if not isinstance(data, types.GeneratorType):
                if str(data).strip():
                    data = json.dumps(data)
        elif headers['Content-Type'].find("application/x-www-form-urlencoded") != -1:
            data = utf8_urlencode(data)
    else:
        data = utf8_urlencode(data)

    return data
