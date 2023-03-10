from os.path import abspath
from pathlib import Path
import sys

sys.path.append(abspath(Path(__file__, "../../")))

from env import config
import jwt
import json
from datetime import datetime, timedelta
from functools import wraps
from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework import status


def create_access_token(payload):
    payload.update({"exp": datetime.utcnow() + timedelta(minutes=30)})
    token = jwt.encode(payload, key=config.SECRET_KEY)
    return token


def create_refresh_token(payload):
    payload.update({"exp": datetime.utcnow() + config.TOKEN_MAXAGE})
    token = jwt.encode(payload, key=config.SECRET_KEY)
    return token


def verify(token):
    return jwt.decode(token, key=config.SECRET_KEY, algorithms="HS256")


def verify_access(func):
    @wraps(func)
    def wrapper_function(req, *args, **kwargs):
        try:
            access_token = req.COOKIES["jwt"]
            payload = verify(access_token)
            # req.GET.update({"member_id":payload["id"]})
            # req.data["id"] = payload["id"]
        except jwt.ExpiredSignatureError:  # 시간만료
            return redirect("refresh")
        except Exception as e:
            print("ERROR :", e)
            res = redirect("member:sign_in")
            res.status_code = status.HTTP_401_UNAUTHORIZED
            return res
        return func(req, *args, **kwargs)

    return wrapper_function


if __name__ == "__main__":
    access_token = create_access_token({"id": 1, "token": "access"})
    print(access_token)

    refresh_token = create_refresh_token({"id": 1, "token": "refresh_token"})
    print(refresh_token)

    access_payload = verify(access_token)
    print(access_payload)

    refresh_payload = verify(refresh_token)
    print(refresh_payload)
