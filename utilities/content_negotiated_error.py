# -*- coding: utf-8 -*-
"""
    utilities.content_negotiated_error
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Content negotiated error responses
    http://flask.pocoo.org/snippets/97/
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from flask import make_response, abort as flask_abort, request
from werkzeug.exceptions import default_exceptions, HTTPException
from flask.exceptions import JSONHTTPException

from app import app


def abort(status_code, body=None, headers={}):
    """
    Content negiate the error response.

    """
    if 'text/html' in request.headers.get("Accept", ""):
        error_cls = HTTPException
    else:
        error_cls = JSONHTTPException

    class_name = error_cls.__name__
    bases = [error_cls]
    attributes = {'code': status_code}

    if status_code in default_exceptions:
        # Mixin the Werkzeug exception
        bases.insert(0, default_exceptions[status_code])

    error_cls = type(class_name, tuple(bases), attributes)
    flask_abort(make_response(error_cls(body), status_code, headers))


@app.route("/test")
def view():
    abort(422, {'errors': dict(password="Wrong password")})


if __name__ == "__main__":
    app.run()
