import time

from flask import request, jsonify, current_app
from itsdangerous import TimedSerializer as Serializer
import jwt
from jwt import exceptions


def create_token(user):
    headers = {
        "alg": "HS256",
        "typ": "JWT",
    }
    payload = {
        "name": user.username,
        "user_id": user.id,
        "expiration": int(time.time() + 60),
        "iss": 'cgy'
    }
    token = jwt.encode(payload=payload, key=current_app.config.get('SECRET_KEY'), algorithm='HS256',
                       headers=headers)
    return token


def validate_token(token):
    payload = None
    msg = '成功'
    try:
        payload = jwt.decode(jwt=token, key=current_app.config.get('SECRET_KEY'), algorithms=['HS256'], issuer='cgy')
    except exceptions.ExpiredSignatureError:
        msg = 'token已失效'
    except jwt.DecodeError:
        msg = 'token认证失败'
    except jwt.InvalidTokenError:
        msg = '非法的token'
    return payload, msg


# 在上面的基础上导入


