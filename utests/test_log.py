import json
import os

from requests import Request

from RequestsLibrary.log import log_request, log_response
from utests import SCRIPT_DIR, mock


@mock.patch("RequestsLibrary.log.logger")
def test_log_request(mocked_logger):
    request = Request(method="get", url="http://mock.rulezz")
    request = request.prepare()
    response = mock.MagicMock()
    response.history = []
    response.request = request
    log_request(response)
    assert mocked_logger.info.call_args[0][0] == (
        f"Request:  {request.method.upper()}\n"
        f"URL:      {request.url} \n"
        f"Path URL: /"
    )

    assert mocked_logger.debug.call_args_list[0][0][0] == f"Headers:  {request.headers}"
    assert mocked_logger.debug.call_args_list[1][0][0] == "Request has no content"


@mock.patch("RequestsLibrary.log.logger")
def test_log_request_with_redirect(mocked_logger):
    request = Request(method="get", url="http://mock.rulezz/redirected")
    request = request.prepare()
    original = Request(method="get", url="http://mock.rulezz/original")
    original = original.prepare()
    response = mock.MagicMock()
    response.request = request
    response0 = mock.MagicMock()
    response0.request = original
    response.history = [response0, mock.MagicMock]
    log_request(response)
    assert mocked_logger.info.call_args[0][0] == (
        f"Request:  {request.method.upper()}\n"
        f"URL:      {response.history[0].request.url} (redirected)\n"
        f"Path URL: {response.history[0].request.path_url}"
    )

    assert mocked_logger.debug.call_args_list[0][0][0] == f"Headers:  {request.headers}"
    assert mocked_logger.debug.call_args_list[1][0][0] == "Request has no content"


@mock.patch("RequestsLibrary.log.logger")
def test_log_response(mocked_logger):
    response = mock.MagicMock()
    response.url = "http://mock.rulezz"
    response.request.method = "GET"
    response.status_code = 200
    response.reason = "OK"
    response.content = b"<html>body</html>"
    response.headers = {
        "Date": "Sun, 10 May 2020 22:31:21 GMT",
        "Expires": "-1",
        "Cache-Control": "private, max-age=0",
        "Content-Type": "text/html; charset=ISO-8859-1",
        "P3P": 'CP="This is not a P3P policy! See g.co/p3phelp for more info."',
        "Content-Encoding": "gzip",
        "Server": "gws",
        "X-XSS-Protection": "0",
        "X-Frame-Options": "SAMEORIGIN",
        "Set-Cookie": "1P_JAR=2020-05-10-22; expires=Tue, 09-Jun-2020 22:31:21 GMT; path=/; domain=.google.it; Secure, NID=204=1JvfFtAYLcnQfWYzh5h0K-PttJP8IvuJdcaej_-utCvMHqavyFkwmthddhQZ-sQ6nZkNCWybVUuzTtaNoEK4TD1FG-TA7QIUR2P6-kj-vN0zkjiS4VdfQbxFnfwtIgkBxFDuoAZsoa_oYm0ODjJ4JAZfdXueqrZJ38tDtIOXpVU; expires=Mon, 09-Nov-2020 22:31:21 GMT; path=/; domain=.google.it; HttpOnly",
        "Alt-Svc": 'h3-27=":443"; ma=2592000,h3-25=":443"; ma=2592000,h3-Q050=":443"; ma=2592000,h3-Q049=":443"; ma=2592000,h3-Q048=":443"; ma=2592000,h3-Q046=":443"; ma=2592000,h3-Q043=":443"; ma=2592000,quic=":443"; ma=2592000; v="46,43"',
        "Transfer-Encoding": "chunked",
    }  # noqa
    log_response(response)
    assert mocked_logger.info.call_args[0][0] == (
        f"Response: {response.request.method.upper()}\n"
        f"URL:      {response.url}\n"
        f"Status:   {response.status_code} - {response.reason}"
    )

    assert (
        mocked_logger.debug.call_args_list[0][0][0] == f"Headers:  {response.headers}"
    )
    assert (
        mocked_logger.debug.call_args_list[1][0][0] == f"Content:  {response.content}"
    )


@mock.patch("RequestsLibrary.log.logger")
def test_log_response_json(mocked_logger):
    response = mock.MagicMock()
    response.url = "http://mock.still.rulezz"
    response.request.method = "GET"
    response.status_code = 201
    response.reason = "OK"
    response.content = b'{"a": "1", "b": "2"}'
    response.text = '{"a": "1", "b": "2"}'
    response.headers = {
        "Date": "Sun, 10 May 2020 22:31:21 GMT",
        "Expires": "-1",
        "Cache-Control": "private, max-age=0",
        "Content-Type": "application/json",
        "P3P": 'CP="This is not a P3P policy! See g.co/p3phelp for more info."',
        "Content-Encoding": "gzip",
        "Server": "gws",
        "X-XSS-Protection": "0",
        "X-Frame-Options": "SAMEORIGIN",
        "Set-Cookie": "1P_JAR=2020-05-10-22; expires=Tue, 09-Jun-2020 22:31:21 GMT; path=/; domain=.google.it; Secure, NID=204=1JvfFtAYLcnQfWYzh5h0K-PttJP8IvuJdcaej_-utCvMHqavyFkwmthddhQZ-sQ6nZkNCWybVUuzTtaNoEK4TD1FG-TA7QIUR2P6-kj-vN0zkjiS4VdfQbxFnfwtIgkBxFDuoAZsoa_oYm0ODjJ4JAZfdXueqrZJ38tDtIOXpVU; expires=Mon, 09-Nov-2020 22:31:21 GMT; path=/; domain=.google.it; HttpOnly",
        "Alt-Svc": 'h3-27=":443"; ma=2592000,h3-25=":443"; ma=2592000,h3-Q050=":443"; ma=2592000,h3-Q049=":443"; ma=2592000,h3-Q048=":443"; ma=2592000,h3-Q046=":443"; ma=2592000,h3-Q043=":443"; ma=2592000,quic=":443"; ma=2592000; v="46,43"',
        "Transfer-Encoding": "chunked",
    }  # noqa
    log_response(response)
    assert mocked_logger.info.call_args[0][0] == (
        f"Response: {response.request.method.upper()}\n"
        f"URL:      {response.url}\n"
        f"Status:   {response.status_code} - {response.reason}"
    )

    assert (
        mocked_logger.debug.call_args_list[0][0][0] == f"Headers:  {response.headers}"
    )
    assert (
        mocked_logger.debug.call_args_list[1][0][0]
        == f"JSON:\n{json.dumps(json.loads(response.text), indent=2)}"
    )


@mock.patch("RequestsLibrary.log.logger")
def test_log_response_json_empty(mocked_logger):
    response = mock.MagicMock()
    response.url = "http://mock.still.rulezz"
    response.request.method = "GET"
    response.status_code = 201
    response.reason = "OK"
    response.content = None
    response.text = None
    response.headers = {
        "Date": "Sun, 10 May 2020 22:31:21 GMT",
        "Expires": "-1",
        "Cache-Control": "private, max-age=0",
        "Content-Type": "application/json",
        "P3P": 'CP="This is not a P3P policy! See g.co/p3phelp for more info."',
        "Content-Encoding": "gzip",
        "Server": "gws",
        "X-XSS-Protection": "0",
        "X-Frame-Options": "SAMEORIGIN",
        "Set-Cookie": "1P_JAR=2020-05-10-22; expires=Tue, 09-Jun-2020 22:31:21 GMT; path=/; domain=.google.it; Secure, NID=204=1JvfFtAYLcnQfWYzh5h0K-PttJP8IvuJdcaej_-utCvMHqavyFkwmthddhQZ-sQ6nZkNCWybVUuzTtaNoEK4TD1FG-TA7QIUR2P6-kj-vN0zkjiS4VdfQbxFnfwtIgkBxFDuoAZsoa_oYm0ODjJ4JAZfdXueqrZJ38tDtIOXpVU; expires=Mon, 09-Nov-2020 22:31:21 GMT; path=/; domain=.google.it; HttpOnly",
        "Alt-Svc": 'h3-27=":443"; ma=2592000,h3-25=":443"; ma=2592000,h3-Q050=":443"; ma=2592000,h3-Q049=":443"; ma=2592000,h3-Q048=":443"; ma=2592000,h3-Q046=":443"; ma=2592000,h3-Q043=":443"; ma=2592000,quic=":443"; ma=2592000; v="46,43"',
        "Transfer-Encoding": "chunked",
    }  # noqa
    log_response(response)
    assert mocked_logger.info.call_args[0][0] == (
        f"Response: {response.request.method.upper()}\n"
        f"URL:      {response.url}\n"
        f"Status:   {response.status_code} - {response.reason}"
    )

    assert (
        mocked_logger.debug.call_args_list[0][0][0] == f"Headers:  {response.headers}"
    )
    assert mocked_logger.debug.call_args_list[1][0][0] == "Response has no content"


@mock.patch("RequestsLibrary.log.logger")
def test_log_response_json_invalid(mocked_logger):
    response = mock.MagicMock()
    response.url = "http://mock.still.rulezz"
    response.request.method = "GET"
    response.status_code = 201
    response.reason = "OK"
    response.content = b"{dasdwda"
    response.text = "{dasdwda"
    response.headers = {
        "Date": "Sun, 10 May 2020 22:31:21 GMT",
        "Expires": "-1",
        "Cache-Control": "private, max-age=0",
        "Content-Type": "application/json",
        "P3P": 'CP="This is not a P3P policy! See g.co/p3phelp for more info."',
        "Content-Encoding": "gzip",
        "Server": "gws",
        "X-XSS-Protection": "0",
        "X-Frame-Options": "SAMEORIGIN",
        "Set-Cookie": "1P_JAR=2020-05-10-22; expires=Tue, 09-Jun-2020 22:31:21 GMT; path=/; domain=.google.it; Secure, NID=204=1JvfFtAYLcnQfWYzh5h0K-PttJP8IvuJdcaej_-utCvMHqavyFkwmthddhQZ-sQ6nZkNCWybVUuzTtaNoEK4TD1FG-TA7QIUR2P6-kj-vN0zkjiS4VdfQbxFnfwtIgkBxFDuoAZsoa_oYm0ODjJ4JAZfdXueqrZJ38tDtIOXpVU; expires=Mon, 09-Nov-2020 22:31:21 GMT; path=/; domain=.google.it; HttpOnly",
        "Alt-Svc": 'h3-27=":443"; ma=2592000,h3-25=":443"; ma=2592000,h3-Q050=":443"; ma=2592000,h3-Q049=":443"; ma=2592000,h3-Q048=":443"; ma=2592000,h3-Q046=":443"; ma=2592000,h3-Q043=":443"; ma=2592000,quic=":443"; ma=2592000; v="46,43"',
        "Transfer-Encoding": "chunked",
    }  # noqa
    log_response(response)
    assert mocked_logger.info.call_args[0][0] == (
        f"Response: {response.request.method.upper()}\n"
        f"URL:      {response.url}\n"
        f"Status:   {response.status_code} - {response.reason}"
    )

    assert (
        mocked_logger.debug.call_args_list[0][0][0] == f"Headers:  {response.headers}"
    )
    assert (
        mocked_logger.debug.call_args_list[1][0][0] == f"Content:  {response.content}"
    )
    assert (
        mocked_logger.warn.call_args[0][0]
        == "Response header indicates JSON data but content can not be decoded."
    )


@mock.patch("RequestsLibrary.log.logger")
def test_log_response_xml(mocked_logger):
    response = mock.MagicMock()
    response.url = "http://mock.still.rulezz"
    response.request.method = "GET"
    response.status_code = 201
    response.reason = "OK"
    response.content = b"<item>test</item>"
    response.text = "<item>test</item>"
    response.headers = {
        "Date": "Sun, 10 May 2020 22:31:21 GMT",
        "Expires": "-1",
        "Cache-Control": "private, max-age=0",
        "Content-Type": "application/xml",
        "P3P": 'CP="This is not a P3P policy! See g.co/p3phelp for more info."',
        "Content-Encoding": "gzip",
        "Server": "gws",
        "X-XSS-Protection": "0",
        "X-Frame-Options": "SAMEORIGIN",
        "Set-Cookie": "1P_JAR=2020-05-10-22; expires=Tue, 09-Jun-2020 22:31:21 GMT; path=/; domain=.google.it; Secure, NID=204=1JvfFtAYLcnQfWYzh5h0K-PttJP8IvuJdcaej_-utCvMHqavyFkwmthddhQZ-sQ6nZkNCWybVUuzTtaNoEK4TD1FG-TA7QIUR2P6-kj-vN0zkjiS4VdfQbxFnfwtIgkBxFDuoAZsoa_oYm0ODjJ4JAZfdXueqrZJ38tDtIOXpVU; expires=Mon, 09-Nov-2020 22:31:21 GMT; path=/; domain=.google.it; HttpOnly",
        "Alt-Svc": 'h3-27=":443"; ma=2592000,h3-25=":443"; ma=2592000,h3-Q050=":443"; ma=2592000,h3-Q049=":443"; ma=2592000,h3-Q048=":443"; ma=2592000,h3-Q046=":443"; ma=2592000,h3-Q043=":443"; ma=2592000,quic=":443"; ma=2592000; v="46,43"',
        "Transfer-Encoding": "chunked",
    }  # noqa
    log_response(response)
    assert mocked_logger.info.call_args[0][0] == (
        f"Response: {response.request.method.upper()}\n"
        f"URL:      {response.url}\n"
        f"Status:   {response.status_code} - {response.reason}"
    )

    assert (
        mocked_logger.debug.call_args_list[0][0][0] == f"Headers:  {response.headers}"
    )
    assert mocked_logger.debug.call_args_list[1][0][0] == "XML:\n<item>test</item>\n"


@mock.patch("RequestsLibrary.log.logger")
def test_log_response_xml_empty(mocked_logger):
    response = mock.MagicMock()
    response.url = "http://mock.still.rulezz"
    response.request.method = "GET"
    response.status_code = 201
    response.reason = "OK"
    response.content = None
    response.text = None
    response.headers = {
        "Date": "Sun, 10 May 2020 22:31:21 GMT",
        "Expires": "-1",
        "Cache-Control": "private, max-age=0",
        "Content-Type": "application/xml",
        "P3P": 'CP="This is not a P3P policy! See g.co/p3phelp for more info."',
        "Content-Encoding": "gzip",
        "Server": "gws",
        "X-XSS-Protection": "0",
        "X-Frame-Options": "SAMEORIGIN",
        "Set-Cookie": "1P_JAR=2020-05-10-22; expires=Tue, 09-Jun-2020 22:31:21 GMT; path=/; domain=.google.it; Secure, NID=204=1JvfFtAYLcnQfWYzh5h0K-PttJP8IvuJdcaej_-utCvMHqavyFkwmthddhQZ-sQ6nZkNCWybVUuzTtaNoEK4TD1FG-TA7QIUR2P6-kj-vN0zkjiS4VdfQbxFnfwtIgkBxFDuoAZsoa_oYm0ODjJ4JAZfdXueqrZJ38tDtIOXpVU; expires=Mon, 09-Nov-2020 22:31:21 GMT; path=/; domain=.google.it; HttpOnly",
        "Alt-Svc": 'h3-27=":443"; ma=2592000,h3-25=":443"; ma=2592000,h3-Q050=":443"; ma=2592000,h3-Q049=":443"; ma=2592000,h3-Q048=":443"; ma=2592000,h3-Q046=":443"; ma=2592000,h3-Q043=":443"; ma=2592000,quic=":443"; ma=2592000; v="46,43"',
        "Transfer-Encoding": "chunked",
    }  # noqa
    log_response(response)
    assert mocked_logger.info.call_args[0][0] == (
        f"Response: {response.request.method.upper()}\n"
        f"URL:      {response.url}\n"
        f"Status:   {response.status_code} - {response.reason}"
    )

    assert (
        mocked_logger.debug.call_args_list[0][0][0] == f"Headers:  {response.headers}"
    )
    assert mocked_logger.debug.call_args_list[1][0][0] == "Response has no content"


@mock.patch("RequestsLibrary.log.logger")
def test_log_response_xml_invalid(mocked_logger):
    response = mock.MagicMock()
    response.url = "http://mock.still.rulezz"
    response.request.method = "GET"
    response.status_code = 201
    response.reason = "OK"
    response.content = b"{dasdwda"
    response.text = "{dasdwda"
    response.headers = {
        "Date": "Sun, 10 May 2020 22:31:21 GMT",
        "Expires": "-1",
        "Cache-Control": "private, max-age=0",
        "Content-Type": "application/xml",
        "P3P": 'CP="This is not a P3P policy! See g.co/p3phelp for more info."',
        "Content-Encoding": "gzip",
        "Server": "gws",
        "X-XSS-Protection": "0",
        "X-Frame-Options": "SAMEORIGIN",
        "Set-Cookie": "1P_JAR=2020-05-10-22; expires=Tue, 09-Jun-2020 22:31:21 GMT; path=/; domain=.google.it; Secure, NID=204=1JvfFtAYLcnQfWYzh5h0K-PttJP8IvuJdcaej_-utCvMHqavyFkwmthddhQZ-sQ6nZkNCWybVUuzTtaNoEK4TD1FG-TA7QIUR2P6-kj-vN0zkjiS4VdfQbxFnfwtIgkBxFDuoAZsoa_oYm0ODjJ4JAZfdXueqrZJ38tDtIOXpVU; expires=Mon, 09-Nov-2020 22:31:21 GMT; path=/; domain=.google.it; HttpOnly",
        "Alt-Svc": 'h3-27=":443"; ma=2592000,h3-25=":443"; ma=2592000,h3-Q050=":443"; ma=2592000,h3-Q049=":443"; ma=2592000,h3-Q048=":443"; ma=2592000,h3-Q046=":443"; ma=2592000,h3-Q043=":443"; ma=2592000,quic=":443"; ma=2592000; v="46,43"',
        "Transfer-Encoding": "chunked",
    }  # noqa
    log_response(response)
    assert mocked_logger.info.call_args[0][0] == (
        f"Response: {response.request.method.upper()}\n"
        f"URL:      {response.url}\n"
        f"Status:   {response.status_code} - {response.reason}"
    )

    assert (
        mocked_logger.debug.call_args_list[0][0][0] == f"Headers:  {response.headers}"
    )
    assert (
        mocked_logger.debug.call_args_list[1][0][0] == f"Content:  {response.content}"
    )
    assert (
        mocked_logger.warn.call_args[0][0]
        == "Response header indicates XML data but content can not be decoded."
    )


@mock.patch("RequestsLibrary.log.logger")
def test_log_response_binary(mocked_logger):
    response = mock.MagicMock()
    response.url = "http://mock.still.rulezz"
    response.request.method = "GET"
    response.status_code = 201
    response.reason = "OK"
    with open(os.path.join(SCRIPT_DIR, "../atests/randombytes.bin"), "rb") as f:
        response.content = f.read()
    response.headers = {
        "Date": "Sun, 10 May 2020 22:31:21 GMT",
        "Expires": "-1",
        "Cache-Control": "private, max-age=0",
        "Content-Type": "application/octet-stream",
        "P3P": 'CP="This is not a P3P policy! See g.co/p3phelp for more info."',
        "Content-Encoding": "gzip",
        "Server": "gws",
        "X-XSS-Protection": "0",
        "X-Frame-Options": "SAMEORIGIN",
        "Set-Cookie": "1P_JAR=2020-05-10-22; expires=Tue, 09-Jun-2020 22:31:21 GMT; path=/; domain=.google.it; Secure, NID=204=1JvfFtAYLcnQfWYzh5h0K-PttJP8IvuJdcaej_-utCvMHqavyFkwmthddhQZ-sQ6nZkNCWybVUuzTtaNoEK4TD1FG-TA7QIUR2P6-kj-vN0zkjiS4VdfQbxFnfwtIgkBxFDuoAZsoa_oYm0ODjJ4JAZfdXueqrZJ38tDtIOXpVU; expires=Mon, 09-Nov-2020 22:31:21 GMT; path=/; domain=.google.it; HttpOnly",
        "Alt-Svc": 'h3-27=":443"; ma=2592000,h3-25=":443"; ma=2592000,h3-Q050=":443"; ma=2592000,h3-Q049=":443"; ma=2592000,h3-Q048=":443"; ma=2592000,h3-Q046=":443"; ma=2592000,h3-Q043=":443"; ma=2592000,quic=":443"; ma=2592000; v="46,43"',
        "Transfer-Encoding": "chunked",
    }  # noqa
    log_response(response)
    assert mocked_logger.info.call_args[0][0] == (
        f"Response: {response.request.method.upper()}\n"
        f"URL:      {response.url}\n"
        f"Status:   {response.status_code} - {response.reason}"
    )

    assert (
        mocked_logger.debug.call_args_list[0][0][0] == f"Headers:  {response.headers}"
    )
    assert (
        mocked_logger.debug.call_args_list[1][0][0] == f"Content:  {response.content}"
    )
