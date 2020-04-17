from RequestsLibrary.log import format_data_to_log_string_according_to_headers
from requests.utils import default_headers

# FIXME those tests are broken because I started a refactor without
# all tests and left the refactor uncompleted so I didn't trust the
# refactor and reverted the code but not the tests :)

def test_format_data_with_data_and_headers_none():
    data = format_data_to_log_string_according_to_headers(None, None)
    assert data is None


def test_format_data_with_headers_none():
    data = format_data_to_log_string_according_to_headers('data', None)
    assert data is None


def test_format_data_with_data_none():
    data = format_data_to_log_string_according_to_headers(None, default_headers())
    assert data is None


#def test_format_data_with_json():
#    headers = default_headers()
#    headers['Content-Type'] = "application/json"
#    data =
#    data = format_data_to_log_string_according_to_headers(None, headers)
#    assert data is None
