from flask import jsonify
from werkzeug.exceptions import HTTPException

class NotFound(HTTPException):
    code = 404
    description = "Resource not found"

class BadRequest(HTTPException):
    code = 400
    description = "Bad request"

class Conflict(HTTPException):
    code = 409
    description = "Conflict"

def register_error_handlers(app):
    for exc in (NotFound, BadRequest, Conflict):
        app.register_error_handler(exc, lambda e: (jsonify({
            "error": e.description, "status": e.code
        }), e.code))
