from database import users_repo
from flask import make_response
import jwt
import os
import bcrypt


def register(username: str, password: str):
    if users_repo.user_exists(username):
        return "User already exists", 401
    hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    users_repo.register(username, hashed_pw)
    secret_key = os.getenv("jwt_secret")
    if secret_key is None:
        raise Exception("jwt_secret env not set")
    encoded_jwt = jwt.encode(
        {"username": username}, secret_key, algorithm="HS256")
    resp = make_response()
    resp.set_cookie("jwt", encoded_jwt)
    return "User registered", 200


def login(username: str, password: str):
    if users_repo.login(username, password):
        secret_key = os.getenv("jwt_secret")
        if secret_key is None:
            raise Exception("jwt_secret env not set")
        encoded_jwt = jwt.encode(
            {"username": username}, secret_key, algorithm="HS256")
        resp = make_response()
        resp.set_cookie("jwt", encoded_jwt)
        return resp

    return "Login failed", 401


def logout():
    resp = make_response()
    resp.set_cookie("jwt", expires=0)
    return resp
