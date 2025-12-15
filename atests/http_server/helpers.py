# -*- coding: utf-8 -*-

"""
httpbin.helpers
~~~~~~~~~~~~~~~

This module provides helper functions for httpbin.
"""

import json
import base64
import re
import time
import os
from hashlib import md5, sha256, sha512
from werkzeug.datastructures import WWWAuthenticate, Authorization

from flask import request, make_response
from six.moves.urllib.parse import urlparse, urlunparse


from .structures import CaseInsensitiveDict


ASCII_ART = r"""
    -=[ teapot ]=-

       _...._
     .'  _ _ `.
    | ."` ^ `". _,
    \_;`"---"`|//
      |       ;/
      \_     _/
        `\"\"\"`
"""

REDIRECT_LOCATION = '/redirect/1'

ENV_HEADERS = (
    'X-Varnish',
    'X-Request-Start',
    'X-Heroku-Queue-Depth',
    'X-Real-Ip',
    'X-Forwarded-Proto',
    'X-Forwarded-Protocol',
    'X-Forwarded-Ssl',
    'X-Heroku-Queue-Wait-Time',
    'X-Forwarded-For',
    'X-Heroku-Dynos-In-Use',
    'X-Forwarded-Protocol',
    'X-Forwarded-Port',
    'X-Request-Id',
    'Via',
    'Total-Route-Time',
    'Connect-Time'
)

ROBOT_TXT = """User-agent: *
Disallow: /deny
"""

ACCEPTED_MEDIA_TYPES = [
    'image/webp',
    'image/svg+xml',
    'image/jpeg',
    'image/png',
    'image/*'
]

ANGRY_ASCII = r"""
          .-''''''-.
        .' _      _ '.
       /   O      O   \\
      :                :
      |                |
      :       __       :
       \  .-"`  `"-.  /
        '.          .'
          '-......-'
     YOU SHOULDN'T BE HERE
"""


def json_safe(string, content_type='application/octet-stream'):
    """Returns JSON-safe version of `string`.

    If `string` is a Unicode string or a valid UTF-8, it is returned unmodified,
    as it can safely be encoded to JSON string.

    If `string` contains raw/binary data, it is Base64-encoded, formatted and
    returned according to "data" URL scheme (RFC2397). Since JSON is not
    suitable for binary data, some additional encoding was necessary; "data"
    URL scheme was chosen for its simplicity.
    """
    try:
        string = string.decode('utf-8')
        json.dumps(string)
        return string
    except (ValueError, TypeError):
        return b''.join([
            b'data:',
            content_type.encode('utf-8'),
            b';base64,',
            base64.b64encode(string)
        ]).decode('utf-8')


def get_files():
    """Returns files dict from request context."""

    files = dict()

    for k in request.files.keys():
        for v in request.files.getlist(k):
            content_type = v.content_type or 'application/octet-stream'
            val = json_safe(v.read(), content_type)
            if files.get(k):
                if not isinstance(files[k], list):
                    files[k] = [files[k]]
                files[k].append(val)
            else:
                files[k] = val

    return files


def get_headers(hide_env=True):
    """Returns headers dict from request context."""

    headers = dict(request.headers.items())

    if hide_env and ('show_env' not in request.args):
        for key in ENV_HEADERS:
            try:
                del headers[key]
            except KeyError:
                pass

    return CaseInsensitiveDict(headers.items())


def semiflatten(multi):
    """Convert a MutiDict into a regular dict. If there are more than one value
    for a key, the result will have a list of values for the key. Otherwise it
    will have the plain value."""
    if multi:
        result = multi.to_dict(flat=False)
        for k, v in result.items():
            if len(v) == 1:
                result[k] = v[0]
        return result
    else:
        return multi


def get_url(request):
    """
    Since we might be hosted behind a proxy, we need to check the
    X-Forwarded-Proto, X-Forwarded-Protocol, or X-Forwarded-SSL headers
    to find out what protocol was used to access us.
    """
    protocol = request.headers.get('X-Forwarded-Proto') or request.headers.get('X-Forwarded-Protocol')
    if protocol is None and request.headers.get('X-Forwarded-Ssl') == 'on':
        protocol = 'https'
    if protocol is None:
        return request.url
    url = list(urlparse(request.url))
    url[0] = protocol
    return urlunparse(url)


def get_dict(*keys, **extras):
    """Returns request dict of given keys."""

    _keys = ('url', 'args', 'form', 'data', 'origin', 'headers', 'files', 'json', 'method')

    assert all(map(_keys.__contains__, keys))
    data = request.data
    form = semiflatten(request.form)

    try:
        _json = json.loads(data.decode('utf-8'))
    except (ValueError, TypeError):
        _json = None

    d = dict(
        url=get_url(request),
        args=semiflatten(request.args),
        form=form,
        data=json_safe(data),
        origin=request.headers.get('X-Forwarded-For', request.remote_addr),
        headers=get_headers(),
        files=get_files(),
        json=_json,
        method=request.method,
    )

    out_d = dict()

    for key in keys:
        out_d[key] = d.get(key)

    out_d.update(extras)

    return out_d


def status_code(code):
    """Returns response object of given status code."""

    redirect = dict(headers=dict(location=REDIRECT_LOCATION))

    code_map = {
        301: redirect,
        302: redirect,
        303: redirect,
        304: dict(data=''),
        305: redirect,
        307: redirect,
        401: dict(headers={'WWW-Authenticate': 'Basic realm="Fake Realm"'}),
        402: dict(
            data='Fuck you, pay me!',
            headers={
                'x-more-info': 'http://vimeo.com/22053820'
            }
        ),
        406: dict(data=json.dumps({
                'message': 'Client did not request a supported media type.',
                'accept': ACCEPTED_MEDIA_TYPES
            }),
            headers={
                'Content-Type': 'application/json'
            }),
        407: dict(headers={'Proxy-Authenticate': 'Basic realm="Fake Realm"'}),
        418: dict(  # I'm a teapot!
            data=ASCII_ART,
            headers={
                'x-more-info': 'http://tools.ietf.org/html/rfc2324'
            }
        ),

    }

    r = make_response()
    r.status_code = code

    if code in code_map:

        m = code_map[code]

        if 'data' in m:
            r.data = m['data']
        if 'headers' in m:
            r.headers = m['headers']

    return r


def __parse_request_range(range_header_text):
    """ Return a tuple describing the byte range requested in a GET request
    If the range is open ended on the left or right side, then a value of None
    will be set.
    RFC7233: http://svn.tools.ietf.org/svn/wg/httpbis/specs/rfc7233.html#header.range
    Examples:
      Range : bytes=1024-
      Range : bytes=10-20
      Range : bytes=-999
    """

    left = None
    right = None

    if not range_header_text:
        return left, right

    range_header_text = range_header_text.strip()
    if not range_header_text.startswith('bytes'):
        return left, right

    components = range_header_text.split("=")
    if len(components) != 2:
        return left, right

    components = components[1].split("-")

    try:
        right = int(components[1])
    except:
        pass

    try:
        left = int(components[0])
    except:
        pass

    return left, right


def get_request_range(request_headers, upper_bound):
    first_byte_pos, last_byte_pos = __parse_request_range(request_headers['range'])

    if first_byte_pos is None and last_byte_pos is None:
        # Request full range
        first_byte_pos = 0
        last_byte_pos = upper_bound - 1
    elif first_byte_pos is None:
        # Request the last X bytes
        first_byte_pos = max(0, upper_bound - last_byte_pos)
        last_byte_pos = upper_bound - 1
    elif last_byte_pos is None:
        # Request the last X bytes
        last_byte_pos = upper_bound - 1

    return first_byte_pos, last_byte_pos


def parse_multi_value_header(header_str):
    """Break apart an HTTP header string that is potentially a quoted,
    comma separated list as used in entity headers in RFC2616."""
    parsed_parts = []
    if header_str:
        parts = header_str.split(',')
        for part in parts:
            match = re.search(r'\s*(W/)?\"?([^"]*)\"?\s*', part)
            if match is not None:
                parsed_parts.append(match.group(2))
    return parsed_parts


def next_stale_after_value(stale_after):
    try:
        stal_after_count = int(stale_after) - 1
        return str(stal_after_count)
    except ValueError:
        return 'never'
