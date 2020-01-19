# This code is part of httpbin project source code https://github.com/postmanlabs/httpbin
# See AUTHORS and LICENSE for more information

from flask import Flask, jsonify as flask_jsonify
from .helpers import get_dict


app = Flask(__name__)


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


@app.route("/anything", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "TRACE"])
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
