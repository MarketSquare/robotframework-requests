from requests.status_codes import codes


def parse_named_status(status_code):
    status_code = status_code.lower().replace(' ', '_')
    return codes.get(status_code)
