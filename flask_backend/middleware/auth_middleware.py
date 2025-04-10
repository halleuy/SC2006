from functools import wraps
from flask import request
import jwt
import os


def jwt_required(f):
    @wraps(f)
    def authenticate():
        if "jwt" not in request.cookies:
            return "Login required", 401
        token = request.cookies["jwt"]
        token_data = None

        secret_key = os.getenv("jwt_secret")
        if secret_key is None:
            raise Exception("jwt_secret env not set")
        try:
            token_data = jwt.decode(token, secret_key, algorithms="HS256")
        except Exception:
            return "Login required", 401
        return f(token_data["username"])
    return authenticate
