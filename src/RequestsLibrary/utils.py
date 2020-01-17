from requests.status_codes import codes


class UnknownStatusError(Exception):
    pass


def parse_named_status(status_code):
    """
    Converts named status status from human readable to integer
    """
    code = status_code.lower().replace(' ', '_')
    code = codes.get(code)
    if not code:
        raise UnknownStatusError(status_code)
    return code
