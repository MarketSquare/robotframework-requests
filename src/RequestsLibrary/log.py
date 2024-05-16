from json import JSONDecodeError, dumps, loads

from lxml.etree import XML, XMLSyntaxError, tostring
from requests import JSONDecodeError as RequestsJSONDecodeError
from robot.api import logger

from RequestsLibrary.utils import is_file_descriptor


def log_body(content: bytes, content_type: str) -> str:
    if "application/xml" in content_type.lower():
        try:
            logger.debug(
                f"XML:\n{tostring(XML(content), pretty_print=True, encoding=str)}"
            )
        except (ValueError, XMLSyntaxError):
            logger.warn(
                "Response header indicates XML data but content can not be decoded."
            )
            logger.debug(f"Content:  {content}")
    elif "application/json" in content_type.lower():
        try:
            logger.debug(f"JSON:\n{dumps(loads(content), indent=2)}")
        except (JSONDecodeError, RequestsJSONDecodeError, TypeError):
            logger.warn(
                "Response header indicates JSON data but content can not be decoded."
            )
            logger.debug(f"Content:  {content}")
    else:
        logger.debug(f"Content:  {content}")


def log_response(response):
    logger.info(
        (
            f"Response: {response.request.method.upper()}\n"
            f"URL:      {response.url}\n"
            f"Status:   {response.status_code} - {response.reason}"
        )
    )
    logger.debug(f"Headers:  {response.headers}")
    if response.content:
        try:
            content_type = response.headers["Content-Type"]
        except KeyError:
            content_type = None

        if content_type:
            log_body(response.content, content_type)
        else:
            logger.debug(f"Content:  {response.content}")
    else:
        logger.debug("Response has no content")


def log_request(response):
    request = response.request
    if response.history:
        original_request = response.history[0].request
        redirected = "(redirected)"
    else:
        original_request = request
        redirected = ""

    logger.info(
        (
            f"Request:  {original_request.method.upper()}\n"
            f"URL:      {original_request.url} {redirected}\n"
            f"Path URL: {original_request.path_url}"
        )
    )
    logger.debug(f"Headers:  {original_request.headers}")
    if request.body:
        try:
            content_type = request.headers["Content-Type"]
        except KeyError:
            content_type = None

        if content_type:
            log_body(request.body, content_type)
        else:
            logger.debug(f"Content:  {request.body}")
    else:
        logger.debug("Request has no content")
