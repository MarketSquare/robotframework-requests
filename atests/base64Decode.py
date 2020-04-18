import base64


def base64_decode_data(s):
    # We expect base64 string retrieved from json.data(), which also includes
    # MIME headers in a form "data:application/octet-stream;base64,<ACTUAL BASE64 DATA>"
    # Therefore we strip the headers and decode the actual data
    return base64.b64decode(s.split(',')[1])
