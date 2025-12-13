# This code is part of httpbin project source code https://github.com/postmanlabs/httpbin
# See AUTHORS and LICENSE for more information

from flask import Flask, Response, jsonify as flask_jsonify, request
from flask_httpauth import HTTPBasicAuth, HTTPDigestAuth

from .structures import CaseInsensitiveDict
from .helpers import get_dict, status_code
from .utils import weighted_choice


app = Flask(__name__)
app.config['SECRET_KEY'] = 'test-secret-key-for-digest-auth'

# Initialize authentication handlers
basic_auth = HTTPBasicAuth()
digest_auth = HTTPDigestAuth()


def jsonify(*args, **kwargs):
    response = flask_jsonify(*args, **kwargs)
    if not response.data.endswith(b"\n"):
        response.data += b"\n"
    return response


@app.route("/")
def index():
    return "Flask Http Test Server"


@app.route("/headers")
def view_headers():
    """Return the incoming request's HTTP headers.
    ---
    tags:
      - Request inspection
    produces:
      - application/json
    responses:
      200:
        description: The request's headers.
    """

    return jsonify(get_dict('headers'))


@app.route("/anything", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "TRACE", "HEAD", "CONNECT"])
def view_anything(anything=None):
    """Returns anything passed in request data.
    ---
    tags:
      - Anything
    produces:
      - application/json
    responses:
      200:
        description: Anything passed in request
    """

    return jsonify(
        get_dict(
            "url",
            "args",
            "headers",
            "origin",
            "method",
            "form",
            "data",
            "files",
            "json",
        )
    )


@app.route(
    "/status/<codes>", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "TRACE", "HEAD", "CONNECT"]
)
def view_status_code(codes):
    """Return status code or random status code if more than one are given
    ---
    tags:
      - Status codes
    parameters:
      - in: path
        name: codes
    produces:
      - text/plain
    responses:
      100:
        description: Informational responses
      200:
        description: Success
      300:
        description: Redirection
      400:
        description: Client Errors
      500:
        description: Server Errors
    """

    if "," not in codes:
        try:
            code = int(codes)
        except ValueError:
            return Response("Invalid status code", status=400)
        return status_code(code)

    choices = []
    for choice in codes.split(","):
        if ":" not in choice:
            code = choice
            weight = 1
        else:
            code, weight = choice.split(":")

        try:
            choices.append((int(code), float(weight)))
        except ValueError:
            return Response("Invalid status code", status=400)

    code = weighted_choice(choices)

    return status_code(code)


@app.route("/redirect-to", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "TRACE", "HEAD", "CONNECT", "OPTIONS"])
def redirect_to():
    """302/3XX Redirects to the given URL.
    ---
    tags:
      - Redirects
    produces:
      - text/html
    get:
      parameters:
        - in: query
          name: url
          type: string
          required: true
        - in: query
          name: status_code
          type: int
    post:
      consumes:
        - application/x-www-form-urlencoded
      parameters:
        - in: formData
          name: url
          type: string
          required: true
        - in: formData
          name: status_code
          type: int
          required: false
    patch:
      consumes:
        - application/x-www-form-urlencoded
      parameters:
        - in: formData
          name: url
          type: string
          required: true
        - in: formData
          name: status_code
          type: int
          required: false
    put:
      consumes:
        - application/x-www-form-urlencoded
      parameters:
        - in: formData
          name: url
          type: string
          required: true
        - in: formData
          name: status_code
          type: int
          required: false
    responses:
      302:
        description: A redirection.
    """

    args_dict = request.args.items()
    args = CaseInsensitiveDict(args_dict)

    # We need to build the response manually.
    # This endpoint should set the Location
    # header to the exact string supplied.
    response = app.make_response("")
    response.status_code = 302
    if "status_code" in args:
        status_code = int(args["status_code"])
        if status_code >= 300 and status_code < 400:
            response.status_code = status_code
    response.headers["Location"] = args["url"]

    return response


# Basic auth verification callback
@basic_auth.verify_password
def verify_basic_password(username, password):
    # Get expected credentials from the request path
    path_parts = request.path.split('/')
    if len(path_parts) >= 4 and path_parts[1] == 'basic-auth':
        expected_user = path_parts[2]
        expected_pass = path_parts[3]
        return username == expected_user and password == expected_pass
    return False


@app.route("/basic-auth/<user>/<passwd>")
@basic_auth.login_required
def basic_auth_endpoint(user, passwd):
    """Prompts the user for authorization using HTTP Basic Auth.
    ---
    tags:
      - Auth
    parameters:
      - in: path
        name: user
        type: string
        required: true
      - in: path
        name: passwd
        type: string
        required: true
    produces:
      - application/json
    responses:
      200:
        description: Successful authentication.
      401:
        description: Unsuccessful authentication.
    """
    return jsonify(authenticated=True, user=basic_auth.current_user())


# Digest auth password callback
@digest_auth.get_password
def get_digest_password(username):
    # Get expected credentials from the request path
    path_parts = request.path.split('/')
    if len(path_parts) >= 5 and path_parts[1] == 'digest-auth':
        expected_user = path_parts[3]
        expected_pass = path_parts[4]
        if username == expected_user:
            return expected_pass
    return None


@app.route("/digest-auth/<qop>/<user>/<passwd>")
@app.route("/digest-auth/<qop>/<user>/<passwd>/<algorithm>")
@digest_auth.login_required
def digest_auth_endpoint(qop, user, passwd, algorithm='MD5'):
    """Prompts the user for authorization using HTTP Digest Auth.
    ---
    tags:
      - Auth
    parameters:
      - in: path
        name: qop
        type: string
        required: true
      - in: path
        name: user
        type: string
        required: true
      - in: path
        name: passwd
        type: string
        required: true
      - in: path
        name: algorithm
        type: string
        required: false
        default: MD5
    produces:
      - application/json
    responses:
      200:
        description: Successful authentication.
      401:
        description: Unsuccessful authentication.
    """
    return jsonify(authenticated=True, user=digest_auth.current_user())
